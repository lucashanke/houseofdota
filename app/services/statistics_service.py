from __future__ import division

import datetime
import operator

from app.repositories.match_repository import MatchRepository
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
        matches_played = {}
        matches_won = {}

        for hero in range(0, NUMBER_OF_HEROES +1):
            matches_played[hero] = 0
            matches_won[hero] = 0

        for match in self._matches:
            radiant_win = match.radiant_win
            for slot in match.slots.all():
                matches_played[slot.hero_id] += 1
                if (slot.team == 'radiant' and radiant_win is True) or \
                    (slot.team == 'dire' and radiant_win is False):
                    matches_won[slot.hero_id] += 1

        for hero_id in range(0, NUMBER_OF_HEROES + 1):
            if hero_id in HEROES_LIST:
                played = matches_played[hero_id]
                won = matches_won[hero_id]
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

    def __init__(self, quantity=None):
        self._quantity = quantity

    def _fetch_matches(self):
        return MatchRepository.fetch_latest(self._quantity)

    def get_heroes_statistics(self, matches=None):
        matches = self._fetch_matches() if matches is None else matches
        return HeroesStatistics(matches)
