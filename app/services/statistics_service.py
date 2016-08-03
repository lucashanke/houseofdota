from __future__ import division

import datetime
import operator

from app.repositories.match_repository import MatchRepository
from app.util.dotautil import NUMBER_OF_HEROES

class HeroesStatistics(object):
    def __init__(self, matches):

        self._matches = matches
        self.match_quantity = len(matches)
        self.statistics = []
        self._extract_heroes_statistics()

    def _extract_heroes_statistics(self):
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

        matches_played_sorted = sorted(matches_played.items(), key=operator.itemgetter(1), reverse=True)
        matches_won_sorted = sorted(matches_won.items(), key=operator.itemgetter(1), reverse=True)

        for i in range(0, NUMBER_OF_HEROES +1):
            self.statistics.append({})
            self.statistics[i]['hero_id'] = matches_won_sorted[i][0]
            self.statistics[i]['played'] = matches_played[self.statistics[i]['hero_id']]
            self.statistics[i]['won'] = matches_won[self.statistics[i]['hero_id']]
            self.statistics[i]['pick_rate'] = '{0:.2f}'.format((self.statistics[i]['played']/self._matches.count())*100)
            if self.statistics[i]['played'] is not 0:
                self.statistics[i]['win_rate'] = '{0:.2f}'.format((self.statistics[i]['won']/self.statistics[i]['played'])*100)
            else:
                self.statistics[i]['win_rate'] = 0


class StatisticsService:

    def __init__(self, quantity=None):
        self._quantity = quantity

    def _fetch_matches(self):
        return MatchRepository.fetch_latest(self._quantity)

    def get_heroes_statistics(self, matches=None):
        matches = self._fetch_matches() if matches is None else matches
        return HeroesStatistics(matches)
