import requests
import mock

from django.test import TestCase
from mock import patch
from app.collectors.matches_collector import MatchesCollector
from app.models import Match, Patch
from app.business.match_business import MatchBusiness

class MatchesCollectorTest(TestCase):
    fixtures = ['matches.json']

    def setUp(self):
        self.collector = MatchesCollector(3, ap=True, rap=True)
        self.all_valid_matches = [
            {
                'match_id': 1,
                'start_time': 1457382658,
                'game_mode': 1,
                'lobby_type': 0,
                'players': [
                    {'leaver_status': 0, 'hero_id': 1},
                    {'leaver_status': 0, 'hero_id': 2},
                    {'leaver_status': 0, 'hero_id': 3},
                    {'leaver_status': 0, 'hero_id': 4},
                    {'leaver_status': 0, 'hero_id': 5},
                    {'leaver_status': 0, 'hero_id': 6},
                    {'leaver_status': 0, 'hero_id': 7},
                    {'leaver_status': 0, 'hero_id': 8},
                    {'leaver_status': 0, 'hero_id': 9},
                    {'leaver_status': 0, 'hero_id': 10}
                ]
            },
            {
                'match_id': 2,
                'start_time': 1457382708,
                'game_mode': 22,
                'lobby_type': 0,
                'players': [
                    {'leaver_status': 0, 'hero_id': 1},
                    {'leaver_status': 0, 'hero_id': 2},
                    {'leaver_status': 0, 'hero_id': 3},
                    {'leaver_status': 0, 'hero_id': 4},
                    {'leaver_status': 0, 'hero_id': 5},
                    {'leaver_status': 0, 'hero_id': 6},
                    {'leaver_status': 0, 'hero_id': 7},
                    {'leaver_status': 0, 'hero_id': 8},
                    {'leaver_status': 0, 'hero_id': 9},
                    {'leaver_status': 0, 'hero_id': 10}
                ]
            },
            {
                'match_id': 3,
                'start_time': 1457382710,
                'game_mode': 1,
                'lobby_type': 0,
                'players': [
                    {'leaver_status': 0, 'hero_id': 1},
                    {'leaver_status': 0, 'hero_id': 2},
                    {'leaver_status': 0, 'hero_id': 3},
                    {'leaver_status': 0, 'hero_id': 4},
                    {'leaver_status': 0, 'hero_id': 5},
                    {'leaver_status': 0, 'hero_id': 6},
                    {'leaver_status': 0, 'hero_id': 7},
                    {'leaver_status': 0, 'hero_id': 8},
                    {'leaver_status': 0, 'hero_id': 9},
                    {'leaver_status': 0, 'hero_id': 10}
                ]
            }
        ]

        self.one_repeated_match = [
            {
                'match_id': 1,
                'start_time': 1457382658,
                'game_mode': 1,
                'lobby_type': 0,
                'players': [
                    {'leaver_status': 0, 'hero_id': 1},
                    {'leaver_status': 0, 'hero_id': 2},
                    {'leaver_status': 0, 'hero_id': 3},
                    {'leaver_status': 0, 'hero_id': 4},
                    {'leaver_status': 0, 'hero_id': 5},
                    {'leaver_status': 0, 'hero_id': 6},
                    {'leaver_status': 0, 'hero_id': 7},
                    {'leaver_status': 0, 'hero_id': 8},
                    {'leaver_status': 0, 'hero_id': 9},
                    {'leaver_status': 0, 'hero_id': 10}
                ]
            },
            {
                'match_id': 2,
                'start_time': 1457382708,
                'game_mode': 22,
                'lobby_type': 0,
                'players': [
                    {'leaver_status': 0, 'hero_id': 1},
                    {'leaver_status': 0, 'hero_id': 2},
                    {'leaver_status': 0, 'hero_id': 3},
                    {'leaver_status': 0, 'hero_id': 4},
                    {'leaver_status': 0, 'hero_id': 5},
                    {'leaver_status': 0, 'hero_id': 6},
                    {'leaver_status': 0, 'hero_id': 7},
                    {'leaver_status': 0, 'hero_id': 8},
                    {'leaver_status': 0, 'hero_id': 9},
                    {'leaver_status': 0, 'hero_id': 10}
                ]
            },
            {
                'match_id': 1,
                'start_time': 1457382658,
                'game_mode': 1,
                'lobby_type': 0,
                'players': [
                    {'leaver_status': 0, 'hero_id': 1},
                    {'leaver_status': 0, 'hero_id': 2},
                    {'leaver_status': 0, 'hero_id': 3},
                    {'leaver_status': 0, 'hero_id': 4},
                    {'leaver_status': 0, 'hero_id': 5},
                    {'leaver_status': 0, 'hero_id': 6},
                    {'leaver_status': 0, 'hero_id': 7},
                    {'leaver_status': 0, 'hero_id': 8},
                    {'leaver_status': 0, 'hero_id': 9},
                    {'leaver_status': 0, 'hero_id': 10}
                ]
            }
        ]

        self.one_invalid_match = [
            {
                'match_id': 1,
                'start_time': 1457382658,
                'game_mode': 1,
                'lobby_type': 0,
                'players': [
                    {'leaver_status': 0, 'hero_id': 1},
                    {'leaver_status': 0, 'hero_id': 2},
                    {'leaver_status': 0, 'hero_id': 3},
                    {'leaver_status': 0, 'hero_id': 4},
                    {'leaver_status': 0, 'hero_id': 5},
                    {'leaver_status': 0, 'hero_id': 6},
                    {'leaver_status': 0, 'hero_id': 7},
                    {'leaver_status': 0, 'hero_id': 8},
                    {'leaver_status': 0, 'hero_id': 9},
                    {'leaver_status': 0, 'hero_id': 10}
                ]
            },
            {
                'match_id': 2,
                'start_time': 1457382708,
                'game_mode': 22,
                'lobby_type': 0,
                'players': [
                    {'leaver_status': 0, 'hero_id': 1},
                    {'leaver_status': 0, 'hero_id': 2},
                    {'leaver_status': 0, 'hero_id': 3},
                    {'leaver_status': 0, 'hero_id': 4},
                    {'leaver_status': 0, 'hero_id': 5},
                    {'leaver_status': 0, 'hero_id': 6},
                    {'leaver_status': 0, 'hero_id': 7},
                    {'leaver_status': 0, 'hero_id': 8},
                    {'leaver_status': 0, 'hero_id': 9},
                    {'leaver_status': 0, 'hero_id': 10}
                ]
            },
            {
                'match_id': 3,
                'start_time': 1457382710,
                'game_mode': 1,
                'lobby_type': 0,
                'players': [
                    {'leaver_status': 1, 'hero_id': 1},
                    {'leaver_status': 0, 'hero_id': 2},
                    {'leaver_status': 0, 'hero_id': 3},
                    {'leaver_status': 0, 'hero_id': 4},
                    {'leaver_status': 0, 'hero_id': 5},
                    {'leaver_status': 0, 'hero_id': 6},
                    {'leaver_status': 0, 'hero_id': 7},
                    {'leaver_status': 0, 'hero_id': 8},
                    {'leaver_status': 0, 'hero_id': 9},
                    {'leaver_status': 0, 'hero_id': 10}
                ]
            }
        ]

    @patch('app.collectors.matches_collector.api', autospec=True)
    def test_gmh_from_api_when_succesful_return_gmh_with_status_1(self, mock_api):
        mock_api.get_match_history.return_value = {'result': {'status': 1}}
        self.assertEqual(self.collector.get_gmh_from_api(), {'status': 1})

    @patch('app.collectors.matches_collector.api', autospec=True)
    def test_gmh_from_api_when_status_not_one_return_none(self, mock_api):
        mock_api.get_match_history.return_value = {'result': {'status': 0}}
        self.assertEqual(self.collector.get_gmh_from_api(), None)

    @patch('app.collectors.matches_collector.api', autospec=True)
    def test_gmh_from_api_when_connection_error_return_none(self, mock_api):
        mock_api.get_match_history.side_effect = requests.exceptions.HTTPError()
        self.assertEqual(self.collector.get_gmh_from_api(), None)

    def test_get_matches_from_gmh_when_not_empty_return_matches(self):
        gmh = {
            'status': 0,
            'matches': [
                {
                    'match_id': 1
                }
            ]
        }
        self.assertEqual(self.collector.get_matches_from_history(gmh), [{'match_id': 1}])

    def test_get_matches_from_gmh_when_empty_return_none(self):
        gmh = {
            'status': 0,
            'matches': []
        }
        self.assertEqual(self.collector.get_matches_from_history(gmh), None)

    @patch('app.collectors.matches_collector.api', autospec=True)
    def test_gmd_from_api_when_succesful_return_full_gmd(self, mock_api):
        mock_api.get_match_details.return_value = {'result': {'match_id': 1}}
        self.assertEqual(self.collector.get_gmd_from_api(1), {'match_id': 1})

    @patch('app.collectors.matches_collector.api', autospec=True)
    def test_gmd_from_api_when_connection_error_return_none(self, mock_api):
        mock_api.get_match_details.side_effect = requests.exceptions.HTTPError()
        self.assertEqual(self.collector.get_gmd_from_api(1), None)

    def test_fill_additional_info_return_patch_and_skill_filled(self):
        print(Patch.objects.all())
        self.assertEqual(self.collector.fill_additional_info({'start_time': 1472314312}),
                         {'start_time': 1472314312, 'patch': Patch.objects.get(pk='6.88b'), 'skill': 3})

    @patch.object(MatchesCollector, 'check_if_match_is_recorded', autospec=True)
    @patch.object(MatchesCollector, 'get_gmd_from_api')
    @patch.object(MatchBusiness, 'create_from_json', autospec=False)
    def test_get_and_record_detailed_matches_all_new_return_all(self, mock_create, mock_api, mock_check):
        mock_check.return_value = False
        mock_api.side_effect = self.all_valid_matches
        mock_create.return_value = Match()
        return_matches = [
            {
                'match_id': 1,
                'start_time': 1457382658,
                'game_mode': 1,
                'skill': 3,
                'patch': '6.86f',
                'lobby_type': 0,
                'players': [
                    {'leaver_status': 0, 'hero_id': 1},
                    {'leaver_status': 0, 'hero_id': 2},
                    {'leaver_status': 0, 'hero_id': 3},
                    {'leaver_status': 0, 'hero_id': 4},
                    {'leaver_status': 0, 'hero_id': 5},
                    {'leaver_status': 0, 'hero_id': 6},
                    {'leaver_status': 0, 'hero_id': 7},
                    {'leaver_status': 0, 'hero_id': 8},
                    {'leaver_status': 0, 'hero_id': 9},
                    {'leaver_status': 0, 'hero_id': 10}
                ]
            },
            {
                'match_id': 2,
                'start_time': 1457382708,
                'game_mode': 22,
                'skill': 3,
                'patch': '6.86f',
                'lobby_type': 0,
                'players': [
                    {'leaver_status': 0, 'hero_id': 1},
                    {'leaver_status': 0, 'hero_id': 2},
                    {'leaver_status': 0, 'hero_id': 3},
                    {'leaver_status': 0, 'hero_id': 4},
                    {'leaver_status': 0, 'hero_id': 5},
                    {'leaver_status': 0, 'hero_id': 6},
                    {'leaver_status': 0, 'hero_id': 7},
                    {'leaver_status': 0, 'hero_id': 8},
                    {'leaver_status': 0, 'hero_id': 9},
                    {'leaver_status': 0, 'hero_id': 10}
                ]
            },
            {
                'match_id': 3,
                'start_time': 1457382710,
                'game_mode': 1,
                'skill': 3,
                'patch': '6.86f',
                'lobby_type': 0,
                'players': [
                    {'leaver_status': 0, 'hero_id': 1},
                    {'leaver_status': 0, 'hero_id': 2},
                    {'leaver_status': 0, 'hero_id': 3},
                    {'leaver_status': 0, 'hero_id': 4},
                    {'leaver_status': 0, 'hero_id': 5},
                    {'leaver_status': 0, 'hero_id': 6},
                    {'leaver_status': 0, 'hero_id': 7},
                    {'leaver_status': 0, 'hero_id': 8},
                    {'leaver_status': 0, 'hero_id': 9},
                    {'leaver_status': 0, 'hero_id': 10}
                ]
            }
        ]
        matches = self.collector.get_and_record_detailed_matches(self.all_valid_matches)
        self.assertEqual(len(matches),len(return_matches))

    @patch.object(MatchesCollector, 'check_if_match_is_recorded', autospec=True)
    @patch.object(MatchesCollector, 'get_gmd_from_api')
    @patch.object(MatchBusiness, 'create_from_json', autospec=False)
    def test_get_and_record_detailed_matches_one_repeated_return_list_with_two(self, mock_create, mock_api, mock_check):
        mock_check.side_effect = [False, False, True]
        mock_api.side_effect = self.all_valid_matches
        mock_create.return_value = Match()
        return_matches = [
            {
                'match_id': 1,
                'start_time': 1457382658,
                'game_mode': 1,
                'skill': 3,
                'patch': '6.86f',
                'lobby_type': 0,
                'players': [
                    {'leaver_status': 0, 'hero_id': 1},
                    {'leaver_status': 0, 'hero_id': 2},
                    {'leaver_status': 0, 'hero_id': 3},
                    {'leaver_status': 0, 'hero_id': 4},
                    {'leaver_status': 0, 'hero_id': 5},
                    {'leaver_status': 0, 'hero_id': 6},
                    {'leaver_status': 0, 'hero_id': 7},
                    {'leaver_status': 0, 'hero_id': 8},
                    {'leaver_status': 0, 'hero_id': 9},
                    {'leaver_status': 0, 'hero_id': 10}
                ]
            },
            {
                'match_id': 2,
                'start_time': 1457382708,
                'game_mode': 22,
                'skill': 3,
                'patch': '6.86f',
                'lobby_type': 0,
                'players': [
                    {'leaver_status': 0, 'hero_id': 1},
                    {'leaver_status': 0, 'hero_id': 2},
                    {'leaver_status': 0, 'hero_id': 3},
                    {'leaver_status': 0, 'hero_id': 4},
                    {'leaver_status': 0, 'hero_id': 5},
                    {'leaver_status': 0, 'hero_id': 6},
                    {'leaver_status': 0, 'hero_id': 7},
                    {'leaver_status': 0, 'hero_id': 8},
                    {'leaver_status': 0, 'hero_id': 9},
                    {'leaver_status': 0, 'hero_id': 10}
                ]
            }
        ]
        matches = self.collector.get_and_record_detailed_matches(self.one_repeated_match)
        self.assertEqual(len(matches), len(return_matches))

    @patch.object(MatchesCollector, 'check_if_match_is_recorded', autospec=True)
    @patch.object(MatchesCollector, 'get_gmd_from_api')
    @patch.object(MatchBusiness, 'create_from_json', autospec=False)
    def test_get_and_record_detailed_matches_one_invalid_return_list_with_two(self, mock_create, mock_api, mock_check):
        mock_check.side_effect = [False, False, True]
        mock_api.side_effect = self.all_valid_matches
        mock_create.return_value = Match()
        return_matches = [
            {
                'match_id': 1,
                'start_time': 1457382658,
                'game_mode': 1,
                'skill': 3,
                'patch': '6.86f',
                'lobby_type': 0,
                'players': [
                    {'leaver_status': 0, 'hero_id': 1},
                    {'leaver_status': 0, 'hero_id': 2},
                    {'leaver_status': 0, 'hero_id': 3},
                    {'leaver_status': 0, 'hero_id': 4},
                    {'leaver_status': 0, 'hero_id': 5},
                    {'leaver_status': 0, 'hero_id': 6},
                    {'leaver_status': 0, 'hero_id': 7},
                    {'leaver_status': 0, 'hero_id': 8},
                    {'leaver_status': 0, 'hero_id': 9},
                    {'leaver_status': 0, 'hero_id': 10}
                ]
            },
            {
                'match_id': 2,
                'start_time': 1457382708,
                'game_mode': 22,
                'skill': 3,
                'patch': '6.86f',
                'lobby_type': 0,
                'players': [
                    {'leaver_status': 0, 'hero_id': 1},
                    {'leaver_status': 0, 'hero_id': 2},
                    {'leaver_status': 0, 'hero_id': 3},
                    {'leaver_status': 0, 'hero_id': 4},
                    {'leaver_status': 0, 'hero_id': 5},
                    {'leaver_status': 0, 'hero_id': 6},
                    {'leaver_status': 0, 'hero_id': 7},
                    {'leaver_status': 0, 'hero_id': 8},
                    {'leaver_status': 0, 'hero_id': 9},
                    {'leaver_status': 0, 'hero_id': 10}
                ]
            }
        ]
        matches = self.collector.get_and_record_detailed_matches(self.one_invalid_match)
        self.assertEqual(len(matches), len(return_matches))
