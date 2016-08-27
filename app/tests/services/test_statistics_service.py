import mock

from django.test import TestCase
from mock import patch

from app.models import Match
from app.services.statistics_service import HeroesStatistics
from app.util.dota_util import HEROES_LIST

class HeroesStatisticsServiceTest(TestCase):
    fixtures = ['matches.json']

    def test_extract_heroes_statistics_for_two_matches(self):
        matches = Match.objects.all()
        hero_statistics = HeroesStatistics()
        twice_picked = list(filter(lambda s: s['played'] == 2, hero_statistics.statistics))
        picked = list(filter(lambda s: s['pick_rate'] == 100, hero_statistics.statistics))
        won_all = list(filter(lambda s: s['win_rate'] == 100, hero_statistics.statistics))
        won_half = list(filter(lambda s: s['win_rate'] == 50, hero_statistics.statistics))
        self.assertEqual(len(twice_picked), 10)
        self.assertEqual(len(picked), 10)
        self.assertEqual(len(won_all), 0)
        self.assertEqual(len(won_half), 10)
