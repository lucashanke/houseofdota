from __future__ import division

import datetime
import operator
import pdb

from app.repositories.match_repository import MatchRepository
from app.models import Patch
from app.util.dota_util import NUMBER_OF_HEROES, HEROES_LIST

class HeroesStatistics(object):

    def __new__(self):
        self.statistics = self._extract_heroes_statistics(self)
        return self

    def _extract_heroes_statistics(self):
        statistics = []
        match_quantity = len((MatchRepository.fetch_from_patch(Patch.get_current_patch())))
        heroes_matches = MatchRepository.get_heroes_matches(Patch.get_current_patch())

        for hero_id in range(0, NUMBER_OF_HEROES + 1):
            if hero_id in heroes_matches:
                played = heroes_matches[hero_id]['played']
                won = heroes_matches[hero_id]['won']
                hero_data = {
                    'hero_id': hero_id,
                    'hero_name': HEROES_LIST[hero_id]['localized_name'],
                    'played': played,
                    'won': won,
                    'pick_rate' : (played/match_quantity)*100,
                    'win_rate': (won/played)*100 if played is not 0 else 0
                }
                statistics.append(hero_data)

        return statistics


class StatisticsService:

    def get_heroes_statistics(self):
        return HeroesStatistics()
