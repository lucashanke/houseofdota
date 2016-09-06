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

    def get_counter_pick_statistics(self, hero_id):
        counter_picks = []
        patch_statistics = PatchStatisticsRepository.fetch_patch_statistics(self._patch)

        hero_counters = patch_statistics.counter_statistics.filter(hero=hero_id).order_by('counter')
        hero_victories = patch_statistics.counter_statistics.filter(counter=hero_id).order_by('hero')

        for counter in zip(hero_counters, hero_victories):
            hero_data = {
                'counter_id': counter[0].counter,
                'counter_name': HEROES_LIST[counter[0].counter]['localized_name'],
                'support' : counter[0].support*100,
                'confidence_hero': counter[0].confidence_hero*100,
                'confidence_counter': counter[0].confidence_counter*100,
                'lift': counter[0].lift,
                'counter_coefficient': counter[0].lift*counter[0].support/counter[1].support
            }
            counter_picks.append(hero_data)

        return {
            'match_quantity' : patch_statistics.match_quantity,
            'counter_picks' : sorted(counter_picks, key=lambda c: c['counter_coefficient'], reverse=True)
        }
