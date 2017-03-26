from __future__ import division
from django.db.models import Q

from app.repositories.match_repository import MatchRepository
from app.repositories.patch_statistics_repository import PatchStatisticsRepository
from app.business.statistics_business import StatisticsBusiness
from app.util.dota_util import HEROES_LIST

class StatisticsService:

    def __init__(self, patch):
        self._patch = patch

    def get_heroes_statistics(self, bundle_size):
        statistics = []
        patch_statistics = PatchStatisticsRepository.fetch_patch_statistics(self._patch)

        for heroes_statistics in patch_statistics.heroes_statistics.filter(
                bundle_size=bundle_size).order_by('-confidence')[:150]:
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

    def get_heroes_statistics_recommendation(self, hero_ids):
        statistics = []
        patch_statistics = PatchStatisticsRepository.fetch_patch_statistics(self._patch)

        q_objects = Q()
        for hero in hero_ids:
            q_objects.add(
                Q(hero_bundle__regex=r"(^{0},|, {0},|, {0}$|^{0}$)".format(hero)),
                Q.AND
            )

        for heroes_statistics in patch_statistics.heroes_statistics.filter(
                q_objects, bundle_size=len(hero_ids)+1,
            ).order_by('-confidence')[:5]:

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
                'confidence': confidence*100
            }
            statistics.append(hero_data)
        return {
            'match_quantity' : patch_statistics.match_quantity,
            'statistics' : statistics
        }


    def get_counter_pick_statistics(self, hero_id):
        counter_picks = []
        patch_statistics = PatchStatisticsRepository.fetch_patch_statistics(self._patch)

        hero_counters = patch_statistics.counter_statistics.filter(hero=hero_id).order_by('counter')
        hero_as_counters = patch_statistics.counter_statistics.filter(counter=hero_id).order_by('hero')

        for counter, as_counter in zip(hero_counters, hero_as_counters) :
            counterhero_statistics = patch_statistics.heroes_statistics.filter(hero_bundle=counter.counter)[0]
            rate_advantage = counter.support/(counter.support+as_counter.support)
            rate_advantage_normalized = rate_advantage/counterhero_statistics.win_rate
            counter_coefficient = (counter.lift-1)*rate_advantage_normalized;

            hero_data = {
                'counter_id': counter.counter,
                'counter_name': HEROES_LIST[counter.counter]['localized_name'],
                'support' : counter.support*100,
                'confidence_hero': counter.confidence_hero*100,
                'confidence_counter': counter.confidence_counter*100,
                'lift': counter.lift,
                'counter_coefficient': counter_coefficient,
                'rate_advantage_normalized': rate_advantage_normalized 
            }
            counter_picks.append(hero_data)

        return {
            'match_quantity' : patch_statistics.match_quantity,
            'counter_picks' : sorted(counter_picks, key=lambda c: c['counter_coefficient'], reverse=True)
        }
