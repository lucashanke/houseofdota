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
            heroes = StatisticsBusiness.get_heroes_ids(heroes_statistics)
            heroes_names = StatisticsBusiness.get_heroes_names(heroes_statistics)
            pick_rate = heroes_statistics.pick_rate
            win_rate = heroes_statistics.win_rate
            confidence = heroes_statistics.confidence

            hero_data = {
                'hero_id': heroes,
                'hero_name': heroes_names,
                'pick_rate' : pick_rate*100,
                'win_rate': win_rate*100,
                'confidence': confidence*100
            }
            statistics.append(hero_data)

        return {
            'match_quantity' : patch_statistics.match_quantity,
            'statistics' : statistics
        }
