from __future__ import division

import itertools
from django.db.models import Q

from app.repositories.match_repository import MatchRepository
from app.repositories.patch_statistics_repository import PatchStatisticsRepository
from app.business.statistics_business import StatisticsBusiness, get_heroes_from_association
from app.util.dota_util import HEROES_LIST


class StatisticsService:

    def __init__(self, patch):
        self._patch = patch

    def get_winning_bundles_statistics(self, bundle_size, order_by='-win_rate'):
        statistics = []
        patch_statistics = PatchStatisticsRepository.fetch_patch_statistics(self._patch)
        return {
            'match_quantity': patch_statistics.match_quantity,
            'patch': self._patch.version,
            'statistics': patch_statistics.winning_bundles_statistics.filter(
                bundle_size=bundle_size).order_by(order_by)[:150]
        }
