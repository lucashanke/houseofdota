import datetime
import pytz

from app.models import Match
from app.business.slot_business import SlotBusiness
from app.util.dota_util import GAME_MODES, LOBBY_TYPES

class MatchBusiness:
    @staticmethod
    def create_from_json(match_json):
        utc=pytz.UTC
        match = Match(
            match_id = match_json['match_id'], \
            match_seq_num = match_json['match_seq_num'], \
            radiant_win = match_json['radiant_win'], \
            duration = match_json['duration'], \
            start_time = utc.localize(datetime.datetime.fromtimestamp(match_json['start_time'])), \
            patch = match_json['patch'], \
            tower_status_radiant = match_json['tower_status_radiant'], \
            tower_status_dire = match_json['tower_status_dire'], \
            barracks_status_radiant = match_json['barracks_status_radiant'], \
            barracks_status_dire = match_json['barracks_status_dire'], \
            cluster = match_json['cluster'], \
            first_blood_time = match_json['first_blood_time'], \
            lobby_type = LOBBY_TYPES[match_json['lobby_type']], \
            human_players = match_json['human_players'], \
            leagueid = match_json['leagueid'], \
            game_mode = GAME_MODES[match_json['game_mode']], \
            flags = match_json['flags'], \
            engine = match_json['engine'], \
            radiant_score = match_json['radiant_score'], \
            dire_score = match_json['dire_score'], \
        )
        match.save()
        for slot_json in match_json['players']:
            slot = SlotBusiness.create_from_json(slot_json, match)
        return match

    @staticmethod
    def get_heroes_list(match):
        return [slot.hero_id for slot in match.slots.all()]

    @staticmethod
    def get_winning_team_heroes_list(match):
        team = 'radiant' if match.radiant_win else 'dire'
        return sorted([slot.hero_id for slot in match.slots.filter(team=team)])
