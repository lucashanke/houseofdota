import requests

from dota2py import api
from pymongo import MongoClient
from app.models import Match, Slot
from django.core.exceptions import ObjectDoesNotExist

from app.util.matchutil import is_valid_match, get_match_patch, is_match_from_patch

class CollectorService:
    """Class responsible to collect Dota2 matches according to the desired filters"""

    def __init__(self, skill, patch=None,
                 public=None, league=None, team=None, solo=None, ranked=None,
                 ap=None, cm=None, ar=None, rap=None):
        self._skill = skill
        self._patch = patch

        self._public = public
        self._league = league
        self._team = team
        self._solo = solo
        self._ranked = ranked
        self._ap = ap
        self._ar = ar
        self._cm = cm
        self._rap = rap

        API_KEY = "6A4B23E0046B2FCFAAFD91E8B30904FA"
        api.set_api_key(API_KEY)

        client = MongoClient()
        db = client.house_of_dota
        self.matches_collection = db.matches_collection

    def collect_from_last_100(self):

        gmh = self.get_gmh_from_api()

        matches = self.get_matches_from_history(gmh)

        if matches is None:
            return None
        else:
            print ('%s matches found: ' % len(matches))
            return self.get_and_record_detailed_matches(matches)

    def get_collection_data(self):
        return self.matches_collection.find({})

    def get_gmh_from_api(self):
        try:
            gmh = api.get_match_history(skill=self._skill,
                min_players=10)['result']
        except requests.exceptions.HTTPError as e:
            return None

        error_code = gmh['status']

        if error_code is not 1:
            return None
        else:
            return gmh

    @staticmethod
    def get_gmd_from_api(match_id):
        try:
            gmd = api.get_match_details(match_id)['result']
        except requests.exceptions.HTTPError as e:
            return None
        return gmd

    @staticmethod
    def get_matches_from_history(match_history):

        matches = match_history['matches'] if match_history != {} else None

        if len(matches) is 0:
            return None
        else:
            return matches

    def fill_additional_info_and_record(self, match_json):
        match_json = self.fill_additional_info(match_json)
        match = Match.create_from_json(match_json)
        return match

    def fill_additional_info(self, match_json):
        if self._patch is not None and is_match_from_patch(match_json, self._patch):
            match_json['patch'] = self._patch
        else:
            match_json['patch'] = get_match_patch(match_json)
        match_json['skill'] = self._skill
        return match_json

    def check_and_record_match_details(self, gmd, matches_recorded):
        if is_valid_match(gmd, patch=self._patch, public=self._public, league=self._league, team=self._team,\
                          solo=self._solo, ranked=self._ranked, ap=self._ap, cm=self._cm, ar=self._ar, rap=self._rap):
            recorded = self.fill_additional_info_and_record(gmd)
            if recorded is not None:
                matches_recorded.append(recorded)
        return matches_recorded

    def get_and_record_detailed_matches(self, matches):
        matches_recorded = []
        for match in matches:
            match_id = match['match_id']
            if self.check_if_match_is_recorded(match_id) is False:
                gmd = None
                while gmd is None:
                    gmd = self.get_gmd_from_api(match_id)
                matches_recorded = self.check_and_record_match_details(gmd, matches_recorded)
        return matches_recorded

    def check_if_match_is_recorded(self, match_id):
        try:
            return Match.objects.get(pk=match_id) != None
        except ObjectDoesNotExist as e:
            return False
