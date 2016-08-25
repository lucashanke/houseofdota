from __future__ import unicode_literals

from django.db import models
from django.core.validators import validate_comma_separated_integer_list
from app.util.dotautil import HEROES_LIST, GAME_MODES, LOBBY_TYPES
import datetime

class Match(models.Model):
    match_id = models.BigIntegerField(primary_key=True)
    match_seq_num = models.BigIntegerField(null=True)
    radiant_win = models.BooleanField()
    duration = models.IntegerField(null=True)
    start_time = models.DateTimeField(null=True)
    patch = models.CharField(max_length=255, null=True)
    tower_status_radiant = models.IntegerField(null=True)
    tower_status_dire = models.IntegerField(null=True)
    barracks_status_radiant = models.IntegerField(null=True)
    barracks_status_dire = models.IntegerField(null=True)
    cluster = models.IntegerField(null=True)
    first_blood_time = models.IntegerField(null=True)
    lobby_type = models.CharField(max_length=255,null=True)
    human_players = models.IntegerField(null=True)
    leagueid = models.IntegerField(null=True)
    game_mode = models.CharField(max_length=255,null=True)
    flags = models.IntegerField(null=True)
    engine = models.IntegerField(null=True)
    radiant_score = models.IntegerField(null=True)
    dire_score = models.IntegerField(null=True)
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

    def get_heroes_list(self):
        heroes = []
        for slot in self.slots.all():
            if slot.hero_id is not 0 and slot.hero_id is not None:
                heroes.append(slot.hero_id)
            else:
                return None
        return heroes


class Slot(models.Model):
    match = models.ForeignKey(Match, on_delete=models.CASCADE, related_name='slots')
    team = models.CharField(max_length=10)
    account_id = models.BigIntegerField(null=True)
    hero_id = models.IntegerField()
    items = models.CharField(max_length=255, validators=[validate_comma_separated_integer_list],null=True)
    kills = models.IntegerField(null=True)
    deaths = models.IntegerField(null=True)
    assists = models.IntegerField(null=True)
    leaver_status = models.IntegerField(null=True)
    last_hits = models.IntegerField(null=True)
    denies = models.IntegerField(null=True)
    gpm = models.IntegerField(null=True)
    xpm = models.IntegerField(null=True)
    level = models.IntegerField(null=True)
    gold = models.IntegerField(null=True)
    gold_spent = models.IntegerField(null=True)
    hero_damage = models.IntegerField(null=True)
    tower_damage = models.IntegerField(null=True)
    hero_healing = models.IntegerField(null=True)

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

class NnTrainingResult(models.Model):
    patch = models.CharField(max_length=255)
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    training_matches = models.BigIntegerField()
    testing_matches = models.BigIntegerField()
    training_accuracy = models.FloatField()
    testing_accuracy = models.FloatField()
    radiant_win_test_percentage = models.FloatField()

class Patch(models.Model):
    version = models.CharField(primary_key=True, max_length=255)
    start_date = models.DateTimeField()
