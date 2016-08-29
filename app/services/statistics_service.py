from __future__ import division

from app.repositories.match_repository import MatchRepository
from app.repositories.patch_statistics_repository import PatchStatisticsRepository
from app.util.dota_util import HEROES_LIST

class StatisticsService:

    def __init__(self, patch):
        self._patch = patch

    def get_heroes_statistics(self):
        statistics = []
        patch_statistics = PatchStatisticsRepository.fetch_patch_statistics(self._patch)

        for heroes_statistics in patch_statistics.heroes_statistics.all():
            heroes = int(heroes_statistics.hero_combination)
            heroes_names = HEROES_LIST[heroes]['localized_name']
            played = heroes_statistics.matches_played
            won = heroes_statistics.matches_won
            pick_rate = heroes_statistics.pick_rate
            win_rate = heroes_statistics.win_rate

            hero_data = {
                'hero_id': heroes,
                'hero_name': heroes_names,
                'played': played,
                'won': won,
                'pick_rate' : pick_rate,
                'win_rate': win_rate
            }
            statistics.append(hero_data)

        return {
            'match_quantity' : patch_statistics.match_quantity,
            'statistics' : statistics
        }
