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
        for hero_id in HEROES_LIST.keys():
            self._update_hero_statistics(hero_id, patch_statistics, heroes_rates)

    def _update_hero_statistics(self, hero_id, patch_statistics, rates):
        hero_statistics = patch_statistics.heroes_statistics.filter(hero_combination=hero_id)
        hero_statistics = HeroesStatistics(hero_combination=hero_id,
            patch_statistics=patch_statistics) if len(hero_statistics) == 0 else hero_statistics[0]
        hero_statistics.pick_rate = rates['pick_rate'][hero_id]
        hero_statistics.win_rate = rates['confidence'][hero_id]/rates['pick_rate'][hero_id]
        hero_statistics.confidence = rates['confidence'][hero_id]
        hero_statistics.save()

    def _extract_statistics_from_association_rules(self):
        heroes_rates = { 'pick_rate' : {}, 'win_rate' : {}, 'confidence' : {} }
        picking_data = list(apriori(self._construct_matches_list(), min_support=0.0001, max_length=1))
        for picking_relation in picking_data:
            hero_id, = picking_relation.items
            heroes_rates['pick_rate'][hero_id] = picking_relation.support
        winning_data = list(apriori(self._construct_matches_list_for_winning_teams(), min_support=0.0001, max_length=1))
        for winning_relation in winning_data:
            hero_id, = winning_relation.items
            heroes_rates['confidence'][hero_id] = winning_relation.ordered_statistics[0].confidence
        return heroes_rates

    def _construct_matches_list(self):
        return [ MatchBusiness.get_heroes_list(match) for match in MatchRepository.fetch_from_patch(self._patch) ]

    def _construct_matches_list_for_winning_teams(self):
        return [ MatchBusiness.get_winning_team_heroes_list(match) for match in MatchRepository.fetch_from_patch(self._patch) ]
