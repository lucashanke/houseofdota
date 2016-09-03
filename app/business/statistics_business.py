import itertools
from apyori import apriori

from app.models import HeroesStatistics
from app.business.match_business import MatchBusiness
from app.repositories.match_repository import MatchRepository
from app.repositories.patch_statistics_repository import PatchStatisticsRepository
from app.util.dota_util import HEROES_LIST

class StatisticsBusiness:

    def __init__(self, patch):
        self._patch = patch

    def update_statistics(self):
        patch_statistics = self._update_patch_statistics()
        self._update_heroes_statistics(patch_statistics)

    def _update_patch_statistics(self):
        patch_statistics = PatchStatisticsRepository.fetch_patch_statistics(self._patch)
        match_quantity = len(MatchRepository.fetch_from_patch(self._patch))
        patch_statistics.match_quantity = match_quantity
        patch_statistics.save()
        return patch_statistics

    def _update_heroes_statistics(self, patch_statistics):
        heroes_rates = self._extract_statistics_from_association_rules()
        for hero_ids in heroes_rates['pick_rate'].keys():
            self._update_hero_statistics(hero_ids, patch_statistics, heroes_rates)

    def _update_hero_statistics(self, hero_ids, patch_statistics, rates):
        hero_statistics = patch_statistics.heroes_statistics.filter(hero_bundle=hero_ids)
        hero_statistics = HeroesStatistics(hero_bundle=hero_ids,
            patch_statistics=patch_statistics) if len(hero_statistics) == 0 else hero_statistics[0]
        hero_statistics.pick_rate = rates['pick_rate'][hero_ids]
        hero_statistics.win_rate = rates['confidence'][hero_ids]/rates['pick_rate'][hero_ids]
        hero_statistics.confidence = rates['confidence'][hero_ids]
        hero_statistics.bundle_size = len(hero_ids.split(','))
        hero_statistics.save()

    def _extract_statistics_from_association_rules(self):
        heroes_rates = { 'pick_rate' : {}, 'win_rate' : {}, 'confidence' : {} }
        winning_data = self._extract_association_rules(self._construct_matches_list_for_winning_teams(), 2)
        for winning_association in winning_data:
            hero_ids = self._get_association_heroes(winning_association)
            heroes_rates['confidence'][hero_ids] = winning_association.support
        picking_data = self._extract_association_rules(self._construct_matches_list(), 2)
        for picking_association in picking_data:
            hero_ids = self._get_association_heroes(picking_association)
            if hero_ids in heroes_rates['confidence'].keys():
                heroes_rates['pick_rate'][hero_ids] = picking_association.support
        return heroes_rates

    def _construct_matches_list(self):
        return [ MatchBusiness.get_heroes_list(match) for match in MatchRepository.fetch_from_patch(self._patch) ]

    def _construct_matches_list_for_winning_teams(self):
        return [ MatchBusiness.get_winning_team_heroes_list(match) for match in MatchRepository.fetch_from_patch(self._patch) ]

    def _extract_association_rules(self, matches, max_length):
        return list(apriori(matches, min_support=0.0001, max_length=max_length))

    def _get_association_heroes(self, relation):
        return str(sorted(relation.items)).strip("[]")

    @staticmethod
    def get_heroes_ids(heroes_statistics):
        return [ int(hero_id) for hero_id in heroes_statistics.hero_bundle.split(',') ]

    @staticmethod
    def get_heroes_names(heroes_statistics):
        return [ HEROES_LIST[int(hero_id)]['localized_name'] for hero_id in heroes_statistics.hero_bundle.split(',') ]
