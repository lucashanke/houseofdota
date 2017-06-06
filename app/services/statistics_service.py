from __future__ import division

import itertools
from django.db.models import Q

from app.repositories.match_repository import MatchRepository
from app.repositories.patch_statistics_repository import PatchStatisticsRepository
from app.business.statistics_business import StatisticsBusiness
from app.util.dota_util import HEROES_LIST

class StatisticsService:

    def __init__(self, patch):
        self._patch = patch

    def get_heroes_statistics_bundles(self, bundle_size, order_by='-confidence'):
        statistics = []
        patch_statistics = PatchStatisticsRepository.fetch_patch_statistics(self._patch)

        for heroes_statistics in patch_statistics.heroes_statistics.filter(
                bundle_size=bundle_size).order_by(order_by)[:150]:
            heroes = StatisticsBusiness.get_heroes_bundle(heroes_statistics)
            pick_rate = heroes_statistics.pick_rate
            win_rate = heroes_statistics.win_rate
            confidence = heroes_statistics.confidence

            hero_data = {
                'id': heroes_statistics.id,
                'hero_bundle': heroes,
                'pick_rate' : pick_rate*100,
                'win_rate': win_rate*100,
                'confidence': confidence*100
            }
            statistics.append(hero_data)

        return {
            'match_quantity' : patch_statistics.match_quantity,
            'statistics' : statistics
        }

    def get_bundle_recommendations(self, hero_ids, criteria='-confidence'):
        if len(hero_ids) >= 5:
            return { 'match_quantity': 0, 'statistics' : [] }

        statistics = []
        patch_statistics = PatchStatisticsRepository.fetch_patch_statistics(self._patch)

        heroes_statistics = patch_statistics.heroes_statistics

        for size in reversed(range(len(hero_ids)+1)):
            if len(statistics) >= 10:
                break
            for combination in itertools.combinations(hero_ids, size):
                if len(statistics) >= 10:
                    break
                statistics = statistics + self._get_recommended_for_bundle(
                    combination,
                    heroes_statistics,
                    criteria
                )

        return {
            'match_quantity' : patch_statistics.match_quantity,
            'statistics' : statistics
        }

    def _get_recommended_for_bundle(self, hero_ids, heroes_statistics, criteria='-confidence'):
        statistics = []
        q_objects = Q()
        for hero in hero_ids:
            q_objects.add(
                Q(hero_bundle__regex=r"(^{0},|, {0},|, {0}$|^{0}$)".format(hero)),
                Q.AND
            )

        bundles = heroes_statistics.filter(
            q_objects, bundle_size=len(hero_ids)+1,
        ).order_by(criteria)[:10]

        for heroes_statistics in bundles:
            heroes = StatisticsBusiness.get_heroes_bundle(heroes_statistics)
            pick_rate = heroes_statistics.pick_rate
            win_rate = heroes_statistics.win_rate
            confidence = heroes_statistics.confidence
            hero_data = {
                'id': heroes_statistics.id,
                'hero_bundle': heroes,
                'recommended': [hero for hero in heroes if str(hero['id']) not in hero_ids],
                'pick_rate' : pick_rate*100,
                'win_rate': win_rate*100,
                'confidence': confidence*100,
                'bundle_size': len(hero_ids)+1,
            }
            statistics.append(hero_data)

        return statistics


    def get_hero_counter_pick_statistics(self,
                                         hero_id,
                                         criteria='-lift',
                                         limit=len(HEROES_LIST.keys())
                                         ):
        counter_picks = []
        patch_statistics = PatchStatisticsRepository.fetch_patch_statistics(self._patch)

        hero_counters = patch_statistics.counter_statistics.filter(hero=hero_id).order_by(criteria)[:limit]

        for counter in hero_counters :
            hero_data = {
                'id': counter.counter,
                'hero_id': int(hero_id),
                'name': HEROES_LIST[counter.counter]['localized_name'],
                'support' : counter.support*100,
                'confidence_hero': counter.confidence_hero*100,
                'confidence_counter': counter.confidence_counter*100,
                'lift': counter.lift,
                'counter_coefficient': counter.lift*counter.support*100,
            }
            counter_picks.append(hero_data)

        return {
            'match_quantity' : patch_statistics.match_quantity,
            'counter_picks' : sorted(counter_picks, key=lambda c: c['counter_coefficient'], reverse=True)
        }

    def get_counter_pick_statistics(self, hero_ids):
        return list(map(
            lambda hero: self.get_hero_counter_pick_statistics(hero_id=hero, limit=10), hero_ids
        ))
