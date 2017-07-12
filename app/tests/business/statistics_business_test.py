import mock

from django.test import TestCase
from mock import patch
from app.business.statistics_business import StatisticsBusiness


class CounterAssociationExtractionTest(TestCase):
    @patch('app.business.statistics_business.construct_matches_list', autospec=False)
    def test_extract_counter_for_one_match(self, mock_construct):
        mock_construct.return_value = [[-1, -2, -3, -4, -5, 41, 42, 43, 44, 45]]
        associations = StatisticsBusiness(patch=None).extract_counter_association_rules(1)
        self.assertEqual(associations[0].support, 1.0)
        self.assertEqual(associations[0].lift, 1.0)
        self.assertEqual(associations[0].confidence_counter, 1.0)
        self.assertEqual(associations[0].confidence_hero, 1.0)

    @patch('app.business.statistics_business.construct_matches_list', autospec=False)
    def test_extract_counter_for_one_match_creates_25_rules(self, mock_construct):
        mock_construct.return_value = [[-1, -2, -3, -4, -5, 41, 42, 43, 44, 45]]
        associations = StatisticsBusiness(patch=None).extract_counter_association_rules(1)
        self.assertEqual(len(associations), 25)

    @patch('app.business.statistics_business.construct_matches_list', autospec=False)
    def test_extract_counter_for_two_matches(self, mock_construct):
        mock_construct.return_value = [[-1, -2, -3, -4, -5, 41, 42, 43, 44, 45],
                                       [-41, -2, -3, -4, -5, 1, 42, 43, 44, 45]]
        associations = StatisticsBusiness(patch=None).extract_counter_association_rules(2)
        self.assertEqual(associations[0].counter, 41)
        self.assertEqual(associations[0].hero, 1)
        self.assertEqual(associations[0].support, 0.5)
        self.assertEqual(associations[0].lift, 2.0)
        self.assertEqual(associations[0].confidence_counter, 1.0)
        self.assertEqual(associations[0].confidence_hero, 1.0)

    @patch('app.business.statistics_business.construct_matches_list', autospec=False)
    def test_extract_counter_for_three_matches(self, mock_construct):
        mock_construct.return_value = [[-1, -2, -3, -4, -5, 41, 42, 43, 44, 45],
                                       [-41, -2, -3, -4, -5, 1, 42, 43, 44, 45],
                                       [-1, -2, -3, -4, -5, 41, 42, 43, 44, 45]]
        associations = StatisticsBusiness(patch=None).extract_counter_association_rules(3)
        self.assertEqual(associations[0].counter, 41)
        self.assertEqual(associations[0].hero, 1)
        self.assertEqual(associations[0].support, 1 / 3)
        self.assertEqual(associations[0].confidence_counter, 1.0)
        self.assertEqual(associations[0].confidence_hero, 1.0)
        self.assertEqual(associations[0].lift, 3.0)
