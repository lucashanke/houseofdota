from __future__ import division

import datetime

from .dotautil import NUMBER_OF_HEROES

def is_match_from_patch(match, patch):
    if patch is None:
        return True
    if patch not in patches:
        return False
    start_date = patches[patch]['start_date']
    end_date = patches[patch]['end_date']
    if end_date is None:
        end_date = datetime.datetime.now()
    start_time = match['start_time']
    if start_time is not None:
        match_time = datetime.datetime.fromtimestamp(start_time)
        if start_date < match_time < end_date:
            return True
        else:
            return False
    else:
        return False


def get_match_patch(match):
    for patch in patches:
        if is_match_from_patch(match, patch):
            return patch
    return None


def is_valid_match(gmd, patch=None, public=None, league=None, team=None, solo=None, ranked=None, ap=None, cm=None, ar=None, rap=None):
    return check_lobby_type(gmd, public, league, team, solo, ranked) is True \
        and check_game_mode(gmd, ap, cm, ar, rap) is True \
        and check_abandon(gmd) is False \
        and is_match_from_patch(gmd, patch) is True


def check_lobby_type(match, public=None, league=None, team=None, solo=None, ranked=None):
    if public is None and league is None and team is None and solo is None and ranked is None:
        public = league = team = solo = ranked = True

    if match is not None:
        match_type = match['lobby_type']
        if (public is not None and public and match_type is 0) or \
                (league is not None and league and match_type is 2) or \
                (team is not None and team and match_type is 5) or \
                (solo is not None and solo and match_type is 6) or \
                (ranked is not None and ranked and match_type is 7):
            return True
        return False
    else:
        return None


def check_abandon(match_json):
    if match_json is None:
        return None
    for player in match_json["players"]:
        if player["leaver_status"] != 0 or player['hero_id'] is 0:
            return True
    return False


def check_game_mode(match, ap=None, cm=None, ar=None, rap=None):

    if ap is None and cm is None and ar is None and rap is None:
        ap = cm = ar = rap = True

    game_mode = match["game_mode"]
    if (ap is not None and ap and game_mode is 1) or \
            (cm is not None and cm and game_mode is 2) or \
            (ar is not None and ar and game_mode is 5) or \
            (rap is not None and rap and game_mode is 22):
        return True
    return False


def get_heroes_in_match(match):
    return convert_hero_list(get_heroes_list(match))


def get_heroes_list(match):
    heroes = []
    for player in match['players']:
        if player['hero_id'] is not 0 and player['hero_id'] is not None:
            heroes.append(player['hero_id'])
        else:
            return None
    return heroes


def convert_hero_list(list):
    input = [0] * NUMBER_OF_HEROES

    for id in list:
        if list.index(id) < 5:
            input[id-1] = 1
        else:
            input[id-1] = -1
    return input


def convert_match_result(radiant_win):
    if radiant_win is 1:
        return 1
    else:
        return -1


patches = {
    '6.88b': {
        'start_date': datetime.datetime(2016, 7, 12),
        'end_date': None,
    },
    '6.87': {
        'start_date': datetime.datetime(2016, 4, 25),
        'end_date': datetime.datetime(2016, 7, 12),
    },
    '6.86f': {
        'start_date': datetime.datetime(2016, 2, 21),
        'end_date': datetime.datetime(2016, 4, 25),
    },
    '6.86e': {
        'start_date': datetime.datetime(2016, 2, 5),
        'end_date': datetime.datetime(2016, 2, 21),
    },
    '6.86d': {
        'start_date': datetime.datetime(2016, 1, 20),
        'end_date': datetime.datetime(2016, 2, 5),
    },
    '6.86c': {
        'start_date': datetime.datetime(2015, 12, 29),
        'end_date': datetime.datetime(2016, 1, 20),
    },
    '6.86b': {
        'start_date': datetime.datetime(2015, 12, 20),
        'end_date': datetime.datetime(2015, 12, 29),
    },
    '6.86': {
        'start_date': datetime.datetime(2015, 12, 16),
        'end_date': datetime.datetime(2015, 12, 20),
    },
    '6.85': {
        'start_date': datetime.datetime(2015, 9, 24),
        'end_date': datetime.datetime(2015, 12, 16),
    },
    '6.84c': {
        'start_date': datetime.datetime(2015, 5, 18),
        'end_date': datetime.datetime(2015, 9, 24),
    }
}
