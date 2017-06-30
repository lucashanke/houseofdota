import mock

from django.test import TestCase
from mock import patch
from app.business.statistics_business import StatisticsBusiness

class StatisticsBusinessTest(TestCase):

    @patch.object(StatisticsBusiness, '_construct_matches_list', autospec=False)
    def test_extract_counter_for_one_match(self, mock_construct):
        mock_construct.return_value = [[-1, -2, -3, -4, -5, 41, 42, 43, 44, 45]]
        rates = StatisticsBusiness(patch=None)._extract_counter_picks_from_association_rules(1)
        self.assertEqual(rates['support']['-1, 42'], 1.0)
        self.assertEqual(rates['lift']['-1, 42'], 1.0)
        self.assertEqual(rates['confidence_counter']['-1, 42'], 1.0)
        self.assertEqual(rates['confidence_hero']['-1, 42'], 1.0)

    @patch.object(StatisticsBusiness, '_construct_matches_list', autospec=False)
    def test_extract_counter_for_one_match_does_not_include_non_counters(self, mock_construct):
        mock_construct.return_value = [[-1, -2, -3, -4, -5, 41, 42, 43, 44, 45]]
        rates = StatisticsBusiness(patch=None)._extract_counter_picks_from_association_rules(1)
        self.assertEqual('41, 42' in rates['support'].keys(), False)

    @patch.object(StatisticsBusiness, '_construct_matches_list', autospec=False)
    def test_extract_counter_for_two_matches(self, mock_construct):
        mock_construct.return_value = [[-1, -2, -3, -4, -5, 41, 42, 43, 44, 45],
                                       [-41, -2, -3, -4, -5, 1, 42, 43, 44, 45]]
        rates = StatisticsBusiness(patch=None)._extract_counter_picks_from_association_rules(2)
        self.assertEqual(rates['support']['-1, 42'], 0.5)
        self.assertEqual(rates['lift']['-1, 42'], 1.0)
        self.assertEqual(rates['confidence_counter']['-1, 42'], 1.0)
        self.assertEqual(rates['confidence_hero']['-1, 42'], 0.5)

    @patch.object(StatisticsBusiness, '_construct_matches_list', autospec=False)
    def test_extract_counter_for_three_matches(self, mock_construct):
        mock_construct.return_value = [[-1, -2, -3, -4, -5, 41, 42, 43, 44, 45],
                                       [-41, -2, -3, -4, -5, 1, 42, 43, 44, 45],
                                       [-1, -2, -3, -4, -5, 41, 42, 43, 44, 45]]
        rates = StatisticsBusiness(patch=None)._extract_counter_picks_from_association_rules(3)
        self.assertEqual(rates['support']['-1, 42'], 2/3)
        self.assertEqual(rates['lift']['-1, 42'], 1.0)
        self.assertEqual(rates['confidence_counter']['-1, 42'], 1.0)
        self.assertEqual(rates['confidence_hero']['-1, 42'], 2/3)
