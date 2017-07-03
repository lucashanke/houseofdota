import itertools
from apyori import apriori

from app.models import *
from app.business.match_business import MatchBusiness
from app.repositories.match_repository import MatchRepository
from app.repositories.patch_statistics_repository import PatchStatisticsRepository
from app.util.dota_util import HEROES_LIST

class StatisticsBusiness:

    MAX_MATCHES = 150000
    MAX_BUNDLE_SIZE = 5

    def __init__(self, patch):
        self._patch = patch

    def update_statistics(self):
        matches = MatchRepository.fetch_from_patch(self._patch, max_matches=StatisticsBusiness.MAX_MATCHES)
        patch_statistics = self._update_patch_statistics(matches)
        self._update_heroes_statistics(patch_statistics, matches)
        self._update_counters_statistics(patch_statistics, matches)

    def _update_patch_statistics(self, matches):
        patch_statistics =  PatchStatisticsRepository.fetch_patch_statistics(self._patch)
        patch_statistics.match_quantity = len(matches)
        patch_statistics.save()
        return patch_statistics

    def _update_heroes_statistics(self, patch_statistics, matches):
        heroes_rates = self._extract_statistics_from_association_rules(matches)
        for hero_ids in heroes_rates['pick_rate'].keys():
            self._update_hero_statistics(hero_ids, patch_statistics, heroes_rates)

    def _extract_statistics_from_association_rules(self, matches):
        heroes_rates = { 'pick_rate' : {}, 'win_rate' : {}, 'confidence' : {} }

        winning_data = self._extract_association_rules(self._construct_matches_list_for_winning_teams(matches), StatisticsBusiness.MAX_BUNDLE_SIZE)
        for winning_association in winning_data:
            hero_ids = self._get_association_heroes(winning_association)
            heroes_rates['confidence'][hero_ids] = winning_association.support

        picking_data = self._extract_association_rules(self._construct_teams_list(matches), StatisticsBusiness.MAX_BUNDLE_SIZE)
        for picking_association in picking_data:
            hero_ids = self._get_association_heroes(picking_association)
            if hero_ids in heroes_rates['confidence'].keys():
                heroes_rates['pick_rate'][hero_ids] = picking_association.support*2

        return heroes_rates

    def _update_hero_statistics(self, hero_ids, patch_statistics, rates):
        bundle_rules = patch_statistics.bundle_rules.filter(hero_bundle=hero_ids)
        bundle_rules = BundleAssociationRules(hero_bundle=hero_ids,
            patch_statistics=patch_statistics) if len(bundle_rules) == 0 else bundle_rules[0]
        bundle_rules.pick_rate = rates['pick_rate'][hero_ids]
        bundle_rules.win_rate = rates['confidence'][hero_ids]/rates['pick_rate'][hero_ids]
        bundle_rules.confidence = rates['confidence'][hero_ids]
        bundle_rules.bundle_size = len(hero_ids.split(','))
        bundle_rules.save()

    def _update_counters_statistics(self, patch_statistics, matches):
        counter_rates = self._extract_counter_picks_from_association_rules(matches)
        for hero_ids in counter_rates['support'].keys():
            self._update_counter_statistics(hero_ids, patch_statistics, counter_rates)

    def _extract_counter_picks_from_association_rules(self, matches):
        counter_rates = {
            'support' : {},
            'confidence_counter' : {},
            'confidence_hero' : {},
            'lift': {}
        }
        associations = self._extract_association_rules(self._construct_matches_list(matches, counter_pick=True), 2)
        for association in associations:
            if self._is_counter_association(association):
                hero_ids = self._get_association_heroes(association)
                counter_rates['support'][hero_ids] = association.support
                counter_rates['confidence_counter'][hero_ids] = association.ordered_statistics[0].confidence
                counter_rates['confidence_hero'][hero_ids] = association.ordered_statistics[1].confidence
                counter_rates['lift'][hero_ids] = association.ordered_statistics[0].lift
        return counter_rates

    def _update_counter_statistics(self, hero_ids, patch_statistics, rates):
        counter, hero = [abs(int(hero_id)) for hero_id in hero_ids.split(',')]
        counter_rules = patch_statistics.counter_rules.filter(hero=hero).filter(counter=counter)
        counter_rules = CounterAssociationRules(hero=hero,counter=counter,
            patch_statistics=patch_statistics) if len(counter_rules) == 0 else counter_rules[0]
        counter_rules.support = rates['support'][hero_ids]
        counter_rules.confidence_counter = rates['confidence_counter'][hero_ids]
        counter_rules.confidence_hero = rates['confidence_hero'][hero_ids]
        counter_rules.lift = rates['lift'][hero_ids]
        counter_rules.save()

    def _construct_matches_list(self, matches, counter_pick=False):
        if counter_pick:
            return [ MatchBusiness.get_heroes_list_with_winning_team_info(match) for match in matches ]
        else:
            return [ MatchBusiness.get_heroes_list(match) for match in matches]

    def _construct_teams_list(self, matches):
        return [ team for match in matches for team in MatchBusiness.get_teams_heroes_list(match) ]

    def _construct_matches_list_for_winning_teams(self, matches):
        return [ MatchBusiness.get_winning_team_heroes_list(match) for match in matches ]

    def _extract_association_rules(self, matches, max_length):
        return list(apriori(matches, min_support=0.0001, max_length=max_length))

    def _get_association_heroes(self, association, string=True):
        return str(sorted(association.items)).strip("[]") if string else sorted(association.items)

    def _is_counter_association(self, association):
        hero_ids = self._get_association_heroes(association, string=False)
        return len(hero_ids) == 2 and hero_ids[0] < 0 and hero_ids[1] > 0

    @staticmethod
    def get_heroes_bundle(bundle_rule):
        return [ {
            'id': abs(int(hero_id)),
            'name': HEROES_LIST[abs(int(hero_id))]['localized_name']
        } for hero_id in bundle_rule.hero_bundle.split(',') ]
