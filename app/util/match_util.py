from __future__ import division

import datetime
import pytz

from app.models import Patch

def get_match_patch(match_date):
    utc = pytz.UTC
    #pylint: disable=no-value-for-parameter
    match_date = utc.localize(datetime.datetime.fromtimestamp(match_date))
    for patch in Patch.objects.all().order_by('-start_date'):
        if patch.start_date < match_date:
            return patch
    return None

#pylint: disable=invalid-name,too-many-arguments
def is_valid_match(gmd, public=None, league=None, team=None, solo=None, \
                   ranked=None, ap=None, cm=None, ar=None, rap=None):
    return check_lobby_type(gmd, public, league, team, solo, ranked) is True \
        and check_game_mode(gmd, ap, cm, ar, rap) is True \
        and check_abandon(gmd) is False

#pylint: disable=invalid-name,too-many-arguments
def check_lobby_type(match, public=None, league=None, team=None, solo=None, ranked=None):
    if public is None and league is None and team is None and solo is None and ranked is None:
        public = league = team = solo = ranked = True

    if match is not None:
        match_type = match['lobby_type']
        #pylint: disable=too-many-boolean-expressions
        if (public and match_type == 0) or \
                (league and match_type == 2) or \
                (team and match_type == 5) or \
                (solo and match_type == 6) or \
                (ranked and match_type == 7):
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
    #pylint: disable=too-many-boolean-expressions
    if (ap and game_mode == 1) or \
            (cm and game_mode == 2) or \
            (ar and game_mode == 5) or \
            (rap and game_mode == 22):
        return True
    return False
