from django.test import TestCase

from app.util.match_util import check_lobby_type, check_abandon, \
    check_game_mode, get_match_patch

from app.util.dota_util import NUMBER_OF_HEROES

class MatchUtilTest(TestCase):

    def setUp(self):
        self.match_none = None

        self.match_with_public_lobby = {'lobby_type': 0}
        self.match_with_league_lobby = {'lobby_type': 2}
        self.match_with_team_lobby = {'lobby_type': 5}
        self.match_with_solo_lobby = {'lobby_type': 6}
        self.match_with_ranked_lobby = {'lobby_type': 7}
        self.match_with_invalid_lobby = {'lobby_type': 1}

        self.match_without_abandon_and_selected_hero = {'players': [{'leaver_status': 0, 'hero_id': 1}]}
        self.match_with_disconnect = {'players': [{'leaver_status': 1}]}
        self.match_with_not_selected_hero = {'players': [{'hero_id': 0}]}

        self.match_all_pick = {'game_mode': 1}
        self.match_captains_mode = {'game_mode': 2}
        self.match_all_random = {'game_mode': 5}
        self.match_ranked = {'game_mode': 22}

        self.match_from_688b = {'start_time': 1450396800}

        self.match_with_valid_heroes = {
            'players': [
                {'hero_id': 1},
                {'hero_id': 2},
                {'hero_id': 3},
                {'hero_id': 4},
                {'hero_id': 5},
                {'hero_id': 6},
                {'hero_id': 7},
                {'hero_id': 8},
                {'hero_id': 9},
                {'hero_id': 10},
            ]
        }

        self.match_with_missing_heroes = {
            'players': [
                {'hero_id': 1},
                {'hero_id': 2},
                {'hero_id': 3},
                {'hero_id': 4},
                {'hero_id': 5},
                {'hero_id': 6},
                {'hero_id': 7},
                {'hero_id': 8},
                {'hero_id': 9},
                {'hero_id': 0},
            ]
        }

    def test_check_lobby_with_null_match_should_return_null(self):
        self.assertEqual(check_lobby_type(None), None)

    def test_check_invalid_lobby_should_return_false(self):
        self.assertEqual(check_lobby_type(self.match_with_invalid_lobby), False)

    def test_check_public_lobby_should_return_true(self):
        self.assertEqual(check_lobby_type(self.match_with_public_lobby, public=True), True)

    def test_check_league_lobby_should_return_true(self):
        self.assertEqual(check_lobby_type(self.match_with_league_lobby, league=True), True)

    def test_check_team_lobby_should_return_true(self):
        self.assertEqual(check_lobby_type(self.match_with_team_lobby, team=True), True)

    def test_check_solo_lobby_should_return_true(self):
        self.assertEqual(check_lobby_type(self.match_with_solo_lobby, solo=True), True)

    def test_check_ranked_lobby_should_return_true(self):
        self.assertEqual(check_lobby_type(self.match_with_ranked_lobby, ranked=True), True)

    def test_check_abandon_with_null_match_returns_null(self):
        self.assertEqual(check_abandon(self.match_none), None)

    def test_check_abandon_with_disconnect_return_true(self):
        self.assertEqual(check_abandon(self.match_with_disconnect), True)

    def test_check_abandon_without_disconnect_return_false(self):
        self.assertEqual(check_abandon(self.match_without_abandon_and_selected_hero), False)

    def test_check_game_mode_all_pick_return_true(self):
        self.assertEqual(check_game_mode(self.match_all_pick, ap=True), True)

    def test_check_game_mode_captains_mode_return_true(self):
        self.assertEqual(check_game_mode(self.match_captains_mode, cm=True), True)

    def test_check_game_mode_all_random_return_true(self):
        self.assertEqual(check_game_mode(self.match_all_random, ar=True), True)

    def test_check_game_mode_ranked_return_true(self):
        self.assertEqual(check_game_mode(self.match_ranked, rap=True), True)

    # def test_get_patch_return_686(self):
    #     self.assertEqual(get_match_patch(self.match_from_686), '6.86')
    #
    # def test_get_patch_return_686f(self):
    #     self.assertEqual(get_match_patch(self.match_from_686f), '6.86f')

    # def test_get_heroes_list_return_array_of_heroes_ids(self):
    #     self.assertEqual([1, 2, 3, 4, 5, 6, 7, 8, 9, 10], get_heroes_list(self.match_with_valid_heroes))
    #
    # def test_get_heroes_list_with_missing_hero_return_none(self):
    #     self.assertEqual(None, get_heroes_list(self.match_with_missing_heroes))
    #
    # def test_get_heroes_in_match_return_array_with_heroes_ids_flagged(self):
    #     lineup = [0] * NUMBER_OF_HEROES
    #     lineup[0:9] = [1, 1, 1, 1, 1, -1, -1, -1, -1, -1]
    #     self.assertEqual([1, 2, 3, 4, 5, 6, 7, 8, 9, 10], get_heroes_list(self.match_with_valid_heroes))
    #
    # def test_get_heroes_in_match_with_missing_hero_return_none(self):
    #     self.assertEqual(None, get_heroes_list(self.match_with_missing_heroes))
