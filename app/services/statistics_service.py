from __future__ import division

from app.repositories.patch_statistics_repository import fetch_patch_statistics

#pylint: disable=too-few-public-methods
class StatisticsService:

    def __init__(self, patch):
        self._patch = patch

    def get_winning_bundles_statistics(self, bundle_size, order_by='-win_rate'):
        patch_statistics = fetch_patch_statistics(self._patch)
        return {
            'match_quantity': patch_statistics.match_quantity,
            'patch': self._patch.version,
            'statistics': patch_statistics.winning_bundles_statistics.filter(
                bundle_size=bundle_size).order_by(order_by)[:150]
        }
