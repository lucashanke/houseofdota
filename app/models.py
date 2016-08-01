from __future__ import unicode_literals

from django.db import models
from app.util.dotautil import HEROES_LIST, GAME_MODES, LOBBY_TYPES
import datetime

class Match(models.Model):
    match_id = models.BigIntegerField(primary_key=True)
    match_seq_num = models.BigIntegerField()
    radiant_win = models.BooleanField()
    duration = models.IntegerField()
    start_time = models.DateTimeField()
    patch = models.CharField(max_length=255)
    tower_status_radiant = models.IntegerField()
    tower_status_dire = models.IntegerField()
    barracks_status_radiant = models.IntegerField()
    barracks_status_dire = models.IntegerField()
    cluster = models.IntegerField()
    first_blood_time = models.IntegerField()
    lobby_type = models.CharField(max_length=255)
    human_players = models.IntegerField()
    leagueid = models.IntegerField()
    game_mode = models.CharField(max_length=255)
    flags = models.IntegerField()
    engine = models.IntegerField()
    radiant_score = models.IntegerField()
    dire_score = models.IntegerField()
    pass

    @staticmethod
    def create_from_json(match_json):
        match = Match(
            match_id = match_json['match_id'], \
            match_seq_num = match_json['match_seq_num'], \
            radiant_win = match_json['radiant_win'], \
            duration = match_json['duration'], \
            start_time = datetime.datetime.fromtimestamp(match_json['start_time']), \
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
            slot = Slot.create_from_json(slot_json, match)
        return match


class Slot(models.Model):
    match = models.ForeignKey(Match, on_delete=models.CASCADE)
    team = models.CharField(max_length=10)
    account_id = models.BigIntegerField()
    hero_id = models.IntegerField()
    items = models.CommaSeparatedIntegerField(max_length=255)
    kills = models.IntegerField()
    deaths = models.IntegerField()
    assists = models.IntegerField()
    leaver_status = models.IntegerField()
    last_hits = models.IntegerField()
    denies = models.IntegerField()
    gpm = models.IntegerField()
    xpm = models.IntegerField()
    level = models.IntegerField()
    gold = models.IntegerField()
    gold_spent = models.IntegerField()
    hero_damage = models.IntegerField()
    tower_damage = models.IntegerField()
    hero_healing = models.IntegerField()

    @staticmethod
    def create_from_json(slot_json, match):
        slot = Slot( \
            match = match, \
            team = 'radiant' if slot_json['player_slot'] < 5 else 'dire', \
            account_id = slot_json['account_id'], \
            hero_id = slot_json['hero_id'], \
            items = [slot_json['item_0'], slot_json['item_1'], slot_json['item_2'], \
                     slot_json['item_3'], slot_json['item_4'], slot_json['item_5']], \
            kills = slot_json['kills'], \
            deaths = slot_json['deaths'], \
            assists = slot_json['assists'], \
            leaver_status = slot_json['leaver_status'], \
            last_hits = slot_json['last_hits'], \
            denies = slot_json['denies'], \
            gpm = slot_json['gold_per_min'], \
            xpm = slot_json['xp_per_min'], \
            level = slot_json['level'], \
            gold = slot_json['gold'], \
            gold_spent = slot_json['gold_spent'], \
            hero_damage = slot_json['hero_damage'], \
            tower_damage = slot_json['tower_damage'], \
            hero_healing = slot_json['hero_healing'] \
        )
        slot.save()
