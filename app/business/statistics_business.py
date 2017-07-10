import itertools

from app.models import *
from app.learners.apriori import *
from app.business.match_business import *
from app.business.winning_bundle_statistics_business import *

from app.repositories.match_repository import MatchRepository
from app.repositories.patch_statistics_repository import PatchStatisticsRepository
from app.util.dota_util import HEROES_LIST

def get_heroes_from_association(bundle_association_rule):
    return [ {
        'id': abs(int(hero_id)),
        'name': HEROES_LIST[abs(int(hero_id))]['localized_name']
    } for hero_id in bundle_association_rule.hero_bundle.split(',') ]

def construct_matches_list(matches, counter_pick=False):
    if counter_pick:
        return [ get_heroes_list_with_winning_team_info(match) for match in matches ]
    else:
        return [ get_heroes_list(match) for match in matches]

def construct_matches_list_for_winning_teams(matches):
    return [ get_winning_team_heroes_list(match) for match in matches ]

def construct_teams_list(matches):
    return [
        team for match in matches for team in get_teams_heroes_list(match)
    ]

class StatisticsBusiness:

    MAX_MATCHES = 150000
    MAX_BUNDLE_SIZE = 5

    def __init__(self, patch):
        self._patch = patch
        self._patch_statistics =  PatchStatisticsRepository.fetch_patch_statistics(self._patch)
        if self._patch_statistics is not None:
            self._previous_iteration = self._patch_statistics.iteration
        else:
            self._previous_iteration = 0

    def update_statistics(self):
        matches = MatchRepository.fetch_from_patch(self._patch, max_matches=StatisticsBusiness.MAX_MATCHES)
        self.update_patch_statistics(matches)

    def update_patch_statistics(self, matches):
        self._patch_statistics.match_quantity = len(matches)
        self._patch_statistics.iteration = self._previous_iteration + 1
        self._patch_statistics.save()
        self.update_pick_associations(matches)
        self.update_bundles_associations(matches)
        self.update_counters_associations(matches)
        self.remove_old_association_rules()
        self.update_winning_statistics()
        return self._patch_statistics

    def update_bundles_associations(self, matches):
        heroes_rates = self._extract_statistics_from_association_rules(matches)
        for hero_ids in heroes_rates['pick_rate'].keys():
            self._update_bundle_association(hero_ids, heroes_rates)

    def _extract_statistics_from_association_rules(self, matches):
        heroes_rates = { 'pick_rate' : {}, 'confidence' : {} }

        winning_data = extract_apriori_association_rules(self._construct_matches_list_for_winning_teams(matches), StatisticsBusiness.MAX_BUNDLE_SIZE)
        for winning_association in winning_data:
            hero_ids = get_apriori_association_heroes(winning_association)
            heroes_rates['confidence'][hero_ids] = winning_association.support
            heroes_rates['pick_rate'][hero_ids] = 1

        return heroes_rates

    def _update_bundle_association(self, hero_ids, rates):
        bundle_association = BundleAssociationRules(hero_bundle=hero_ids,
            patch_statistics=self._patch_statistics)
        bundle_association.pick_rate = rates['pick_rate'][hero_ids]
        bundle_association.win_rate = rates['confidence'][hero_ids]/rates['pick_rate'][hero_ids]
        bundle_association.confidence = rates['confidence'][hero_ids]
        bundle_association.bundle_size = len(hero_ids.split(','))
        bundle_association.iteration = self._previous_iteration + 1
        bundle_association.save()

    def update_counters_associations(self, matches):
        counter_associations = self._extract_counter_association_rules(matches)
        for counter_association in counter_associations:
            self._save_counter_rule(counter_association)

    def _extract_counter_association_rules(self, matches):
        apriori_associations = extract_apriori_association_rules(
            self._construct_matches_list(matches, counter_pick=True), 2
        )
        counter_associations = []
        for association in apriori_associations:
            if is_apriori_counter_association(association):
                counter_associations.append(self._build_counter_association_rule(association))
        return counter_associations

    def _build_counter_association_rule(self, association):
        hero_ids = get_apriori_association_heroes(association)
        counter, hero = [abs(int(hero_id)) for hero_id in hero_ids.split(',')]
        counter_rule = CounterAssociationRules(
            hero=hero,
            counter=counter,
            support = association.support,
            confidence_counter = association.ordered_statistics[0].confidence,
            confidence_hero = association.ordered_statistics[1].confidence,
            lift = association.ordered_statistics[0].lift,
            iteration = self._previous_iteration + 1
        )
        return counter_rule

    def _save_counter_rule(self, counter_rule):
        counter_rule.patch_statistics = self._patch_statistics
        counter_rule.save()

    def update_pick_associations(self, matches):
        pick_associations = self._extract_pick_association_rules(matches)
        for pick_association in pick_associations:
            self._save_pick_rule(pick_association)

    def _extract_pick_association_rules(self, matches):
        apriori_associations = extract_apriori_association_rules(
            self._construct_teams_list(matches),
            StatisticsBusiness.MAX_BUNDLE_SIZE,
            min_support=0.00005
        )
        pick_associations = []
        for association in apriori_associations:
            pick_associations.append(self._build_pick_association_rule(association))
        return pick_associations

    def _build_pick_association_rule(self, association):
        hero_ids = get_apriori_association_heroes(association)
        pick_rule = PickAssociationRules(
            hero_bundle=hero_ids,
            bundle_size=len(hero_ids.split(',')),
            support = association.support*2,
            iteration = self._previous_iteration + 1
        )
        return pick_rule

    def _save_pick_rule(self, pick_rule):
        pick_rule.patch_statistics = self._patch_statistics
        pick_rule.save()

    def remove_old_association_rules(self):
        self._patch_statistics.bundle_rules.filter(iteration=self._previous_iteration).delete()
        self._patch_statistics.pick_rules.filter(iteration=self._previous_iteration).delete()
        self._patch_statistics.counter_rules.filter(iteration=self._previous_iteration).delete()

    def update_winning_statistics(self):
        for bundle_association in self._patch_statistics.bundle_rules.all():
            winning_bundle_statistics = calculate_from_association_rule(bundle_association)
            winning_bundle_statistics.iteration = self._previous_iteration + 1
            winning_bundle_statistics.save()
        self._patch_statistics.winning_bundles_statistics.filter(
            iteration=self._previous_iteration
        ).delete()
