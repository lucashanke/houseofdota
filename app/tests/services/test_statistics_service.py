import mock

from django.test import TestCase
from mock import patch

from app.models import Match
from app.services.statistics_service import HeroesStatistics
from app.util.dotautil import HEROES_LIST

class HeroesStatisticsServiceTest(TestCase):
    fixtures = ['matches.json']

    @patch.object(HeroesStatistics, '_extract_heroes_statistics')
    def test_heroes_statistics_when_matches_is_none(self, mock):
        hero_statistics = HeroesStatistics(None)
        self.assertIsNone(hero_statistics)
        self.assertFalse(mock.called)

    @patch.object(HeroesStatistics, '_extract_heroes_statistics')
    def test_heroes_statistics_when_matches_is_empty(self, mock):
        hero_statistics = HeroesStatistics([])
        self.assertIsNone(hero_statistics.statistics)
        self.assertFalse(mock.called)

    @patch.object(HeroesStatistics, '_extract_heroes_statistics')
    def test_heroes_statistics_when_matches_is_valid(self, mock):
        hero_statistics = HeroesStatistics([Match()])
        self.assertIsNotNone(hero_statistics)
        self.assertIsNotNone(hero_statistics.statistics)
        self.assertTrue(mock.called)

    def test_extract_heroes_statistics_for_one_match(self):
        match = Match.objects.all()[0]
        hero_statistics = HeroesStatistics([match])
        picked = list(filter(lambda s: s['pick_rate'] == 100, hero_statistics.statistics))
        won = list(filter(lambda s: s['win_rate'] == 100, hero_statistics.statistics))
        self.assertEqual(len(picked), 10)
        self.assertEqual(len(won), 5)

    def test_extract_heroes_statistics_for_one_match(self):
        match = Match.objects.all()[0]
        hero_statistics = HeroesStatistics([match])
        once_picked = list(filter(lambda s: s['played'] == 1, hero_statistics.statistics))
        not_picked = list(filter(lambda s: s['played'] == 0, hero_statistics.statistics))
        picked = list(filter(lambda s: s['pick_rate'] == 100, hero_statistics.statistics))
        won = list(filter(lambda s: s['win_rate'] == 100, hero_statistics.statistics))
        not_won = list(filter(lambda s: s['win_rate'] == 0, hero_statistics.statistics))
        self.assertEqual(len(once_picked), 10)
        self.assertEqual(len(not_picked), len(HEROES_LIST)-10)
        self.assertEqual(len(picked), 10)
        self.assertEqual(len(won), 5)
        self.assertEqual(len(not_won), len(HEROES_LIST)-5)

    def test_extract_heroes_statistics_for_two_matches(self):
        matches = Match.objects.all()
        hero_statistics = HeroesStatistics(matches)
        twice_picked = list(filter(lambda s: s['played'] == 2, hero_statistics.statistics))
        not_picked = list(filter(lambda s: s['played'] == 0, hero_statistics.statistics))
        picked = list(filter(lambda s: s['pick_rate'] == 100, hero_statistics.statistics))
        won_all = list(filter(lambda s: s['win_rate'] == 100, hero_statistics.statistics))
        won_half = list(filter(lambda s: s['win_rate'] == 50, hero_statistics.statistics))
        not_won = list(filter(lambda s: s['win_rate'] == 0, hero_statistics.statistics))
        self.assertEqual(len(twice_picked), 10)
        self.assertEqual(len(not_picked), len(HEROES_LIST)-10)
        self.assertEqual(len(picked), 10)
        self.assertEqual(len(won_all), 0)
        self.assertEqual(len(won_half), 10)
        self.assertEqual(len(not_won), len(HEROES_LIST)-10)
