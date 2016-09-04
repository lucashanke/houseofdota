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
        counter_rates = self._extract_counter_picks_from_association_rules()
        for hero_ids in counter_rates['pick_rate'].keys():
            self._update_hero_statistics(hero_ids, patch_statistics, counter_rates, counter_rate=True)

    def _update_hero_statistics(self, hero_ids, patch_statistics, rates, counter_rate=False):
        hero_statistics = patch_statistics.heroes_statistics.filter(hero_bundle=hero_ids)
        hero_statistics = HeroesStatistics(hero_bundle=hero_ids,
            patch_statistics=patch_statistics) if len(hero_statistics) == 0 else hero_statistics[0]
        hero_statistics.pick_rate = rates['pick_rate'][hero_ids]
        hero_statistics.win_rate = rates['confidence'][hero_ids]/rates['pick_rate'][hero_ids]
        hero_statistics.confidence = rates['confidence'][hero_ids]
        hero_statistics.bundle_size = len(hero_ids.split(','))
        hero_statistics.counter_pick = counter_rate
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

    def _extract_counter_picks_from_association_rules(self):
        counter_rates = { 'pick_rate' : {}, 'win_rate' : {}, 'confidence' : {} }
        associations = self._extract_association_rules(self._construct_matches_list(counter_pick=True), 2)
        for association in associations:
            if self._is_counter_association(association):
                hero_ids = self._get_association_heroes(association)
                counter_rates['pick_rate'][hero_ids] = association.support
                counter_rates['confidence'][hero_ids] = association.ordered_statistics[0].confidence
        return counter_rates

    def _construct_matches_list(self, counter_pick=False):
        matches = MatchRepository.fetch_from_patch(self._patch)
        if counter_pick:
            return [ MatchBusiness.get_heroes_list_with_winning_team_info(match) for match in matches ]
        else:
            return [ MatchBusiness.get_heroes_list(match) for match in matches]

    def _construct_matches_list_for_winning_teams(self):
        return [ MatchBusiness.get_winning_team_heroes_list(match) for match in MatchRepository.fetch_from_patch(self._patch) ]

    def _extract_association_rules(self, matches, max_length):
        return list(apriori(matches, min_support=0.0001, max_length=max_length))

    def _get_association_heroes(self, association, string=True):
        return str(sorted(association.items)).strip("[]") if string else sorted(association.items)

    def _is_counter_association(self, association):
        hero_ids = self._get_association_heroes(association, string=False)
        return len(hero_ids) == 2 and hero_ids[0] < 0 and hero_ids[1] > 0

    @staticmethod
    def get_heroes_bundle(heroes_statistics):
        return [ {
            'id': abs(int(hero_id)),
            'name': HEROES_LIST[abs(int(hero_id))]['localized_name']
        } for hero_id in heroes_statistics.hero_bundle.split(',') ]
