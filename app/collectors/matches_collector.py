import requests
from dota2py import api
from django.core.exceptions import ObjectDoesNotExist

from app.models import Match
from app.business.match_business import create_from_json
from app.util.match_util import is_valid_match, get_match_patch

def check_if_match_is_recorded(match_id):
    try:
        return Match.objects.get(pk=match_id) is not None
    except ObjectDoesNotExist:
        return False

#pylint: disable=too-many-instance-attributes
class MatchesCollector:
    """Class responsible to collect Dota2 matches according to the desired filters"""

    #pylint: disable=too-many-arguments
    def __init__(self, skill,
                 public=None, league=None, team=None, solo=None, ranked=None,
                 ap=None, cm=None, ar=None, rap=None):
        self._skill = skill

        self._public = public
        self._league = league
        self._team = team
        self._solo = solo
        self._ranked = ranked
        self._ap = ap
        self._ar = ar
        self._cm = cm
        self._rap = rap

        api_key = "6A4B23E0046B2FCFAAFD91E8B30904FA"
        api.set_api_key(api_key)

    def collect_from_last_100(self):

        gmh = self.get_gmh_from_api()

        matches = self.get_matches_from_history(gmh)

        if matches is None:
            return None
        print('%s matches found: ' % len(matches))
        return self.get_and_record_detailed_matches(matches)

    def get_gmh_from_api(self):
        try:
            gmh = api.get_match_history(skill=self._skill,
                                        min_players=10)['result']
        except requests.exceptions.HTTPError:
            return None

        error_code = gmh['status']

        if error_code is not 1:
            return None
        return gmh

    @staticmethod
    def get_gmd_from_api(match_id):
        try:
            gmd = api.get_match_details(match_id)['result']
        except requests.exceptions.HTTPError:
            return None
        return gmd

    @staticmethod
    def get_matches_from_history(match_history):

        matches = match_history['matches'] if match_history != {} else None

        if len(matches) is 0:
            return None
        return matches

    def fill_additional_info(self, match_json):
        match_json['patch'] = get_match_patch(match_json['start_time'])
        match_json['skill'] = self._skill
        return match_json

    def check_and_record_match_details(self, gmd, matches_recorded):
        if is_valid_match(
                gmd,
                public=self._public,
                league=self._league,
                team=self._team,
                solo=self._solo,
                ranked=self._ranked,
                ap=self._ap,
                cm=self._cm,
                ar=self._ar,
                rap=self._rap):
            match_json = self.fill_additional_info(gmd)
            recorded = create_from_json(match_json)
            if recorded is not None:
                matches_recorded.append(recorded)
        return matches_recorded

    def get_and_record_detailed_matches(self, matches):
        matches_recorded = []
        for match in matches:
            match_id = match['match_id']
            if check_if_match_is_recorded(match_id) is False:
                gmd = None
                while gmd is None:
                    gmd = self.get_gmd_from_api(match_id)
                matches_recorded = self.check_and_record_match_details(
                    gmd, matches_recorded)
        return matches_recorded
