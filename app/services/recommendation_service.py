from __future__ import division

import itertools
from django.db.models import Q

from app.repositories.patch_statistics_repository import fetch_patch_statistics
from app.business.statistics_business import get_heroes_from_association
from app.util.dota_util import HEROES_LIST

def counter_coefficient(counter_rule, opposite_rule):
    return counter_rule.lift*counter_rule.support/(opposite_rule.lift*opposite_rule.support)

class RecommendationService:

    def __init__(self, patch):
        self._patch = patch

    def get_bundle_recommendations(self, hero_ids, criteria='-confidence'):
        if len(hero_ids) >= 5:
            return {'match_quantity': 0, 'statistics' : []}

        recommendations = []
        patch_statistics = fetch_patch_statistics(self._patch)

        bundle_association_rules = patch_statistics.bundle_rules
        pick_association_rules = patch_statistics.pick_rules

        for size in reversed(range(len(hero_ids)+1)):
            if len(recommendations) >= 10:
                break
            for combination in itertools.combinations(hero_ids, size):
                if len(recommendations) >= 10:
                    break
                recommendations = recommendations + self._get_recommended_for_bundle(
                    combination,
                    bundle_association_rules,
                    pick_association_rules,
                    criteria
                )

        return {
            'match_quantity' : patch_statistics.match_quantity,
            'patch': self._patch.version,
            'statistics' : recommendations
        }

    #pylint: disable=no-self-use
    def _get_recommended_for_bundle(self, hero_ids, bundle_rules, pick_rules, \
                                    criteria='-confidence'):
        recommendations = []
        q_objects = Q()
        for hero in hero_ids:
            q_objects.add(
                Q(hero_bundle__regex=r"(^{0},|, {0},|, {0}$|^{0}$)".format(hero)),
                Q.AND
            )

        bundle_associations_for_heroes = bundle_rules.filter(
            q_objects, bundle_size=len(hero_ids)+1,
        ).order_by(criteria)[:10]

        for bundle_association in bundle_associations_for_heroes:
            pick_association = pick_rules.filter(
                hero_bundle=bundle_association.hero_bundle
            )
            if len(pick_association) is not 0:
                heroes = get_heroes_from_association(bundle_association)
                pick_rate = pick_association[0].support
                win_rate = bundle_association.confidence/pick_association[0].support
                confidence = bundle_association.confidence
                recommendations.append({
                    'id': bundle_association.id,
                    'hero_bundle': heroes,
                    'recommended': [hero for hero in heroes if str(hero['id']) not in hero_ids],
                    'pick_rate' : pick_rate*100,
                    'win_rate': win_rate*100,
                    'confidence': confidence*100,
                    'bundle_size': len(hero_ids)+1,
                })
        return recommendations


    def _get_hero_counters_recommendations(self,
                                           hero_id,
                                           criteria='lift',
                                           limit=len(HEROES_LIST.keys())):
        counter_picks = []
        patch_statistics = fetch_patch_statistics(self._patch)

        order_by = criteria
        if criteria == 'counter_coefficient':
            order_by = 'lift'

        hero_counters = patch_statistics.counter_rules.filter(
            hero=hero_id).order_by("-{}".format(order_by))[:limit]

        for counter in hero_counters:
            opposite_counter_rule = patch_statistics.counter_rules.filter(
                counter=hero_id, hero=counter.counter)[0]
            hero_data = {
                'id': counter.counter,
                'hero_id': int(hero_id),
                'name': HEROES_LIST[counter.counter]['localized_name'],
                'support' : counter.support*100,
                'confidence_hero': counter.confidence_hero*100,
                'confidence_counter': counter.confidence_counter*100,
                'lift': counter.lift,
                'counter_coefficient': counter_coefficient(counter, opposite_counter_rule)
            }
            counter_picks.append(hero_data)

        return {
            'match_quantity' : patch_statistics.match_quantity,
            'counter_picks' : sorted(counter_picks, key=lambda c: c[criteria], reverse=True)
        }

    def get_counter_recommendations(self, hero_ids):
        return list(map(
            lambda hero: self._get_hero_counters_recommendations(hero_id=hero, limit=10), hero_ids
        ))
