from __future__ import division

import datetime
import operator
import pdb

from app.repositories.match_repository import MatchRepository
from app.models import Patch
from app.util.dota_util import NUMBER_OF_HEROES, HEROES_LIST

class HeroesStatistics(object):

    def __new__(self, matches):
        if matches is None:
            return None
        self._matches = matches
        self.match_quantity = len(matches)
        self.statistics = self._extract_heroes_statistics(self) if self.match_quantity is not 0 else None
        return self

    def _extract_heroes_statistics(self):
        statistics = []

        heroes_matches = MatchRepository.get_heroes_matches(Patch.get_current_patch())

        for hero_id in range(0, NUMBER_OF_HEROES + 1):
            if hero_id in HEROES_LIST:
                played = heroes_matches[hero_id]['played']
                won = heroes_matches[hero_id]['won']
                hero_data = {
                    'hero_id': hero_id,
                    'hero_name': HEROES_LIST[hero_id]['localized_name'],
                    'played': played,
                    'won': won,
                    'pick_rate' : (played/self.match_quantity)*100,
                    'win_rate': (won/played)*100 if played is not 0 else 0
                }
                statistics.append(hero_data)

        return statistics


class StatisticsService:

    def _fetch_matches(self):
        return MatchRepository.fetch_from_patch(Patch.get_current_patch())

    def get_heroes_statistics(self, matches=None):
        matches = self._fetch_matches() if matches is None else matches
        return HeroesStatistics(matches)
