from __future__ import division

import datetime
import pytz

from .dota_util import NUMBER_OF_HEROES
from app.models import Patch

def get_match_patch(match_date):
    utc=pytz.UTC
    match_date = utc.localize(datetime.datetime.fromtimestamp(match_date))
    for patch in Patch.objects.all().order_by('-start_date'):
        if patch.start_date <= match_date:
            return patch
    return None

def is_valid_match(gmd, patch=None, public=None, league=None, team=None, solo=None, ranked=None, ap=None, cm=None, ar=None, rap=None):
    return check_lobby_type(gmd, public, league, team, solo, ranked) is True \
        and check_game_mode(gmd, ap, cm, ar, rap) is True \
        and check_abandon(gmd) is False

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


patches = {
    '6.88c': {
        'start_date': datetime.datetime(2016, 8, 19),
        'end_date': None,
    },
    '6.88b': {
        'start_date': datetime.datetime(2016, 7, 12),
        'end_date': datetime.datetime(2016, 8, 19),
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
