from __future__ import unicode_literals

from django.db import models
from django.core.validators import validate_comma_separated_integer_list

class Patch(models.Model):
    version = models.CharField(primary_key=True, max_length=255)
    start_date = models.DateTimeField()

class Match(models.Model):
    match_id = models.BigIntegerField(primary_key=True)
    match_seq_num = models.BigIntegerField(null=True)
    radiant_win = models.BooleanField()
    duration = models.IntegerField(null=True)
    start_time = models.DateTimeField(null=True)
    patch = models.ForeignKey(Patch, on_delete=models.PROTECT, related_name='matches')
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
    analysed = models.BooleanField(default=False)
    pass


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

class NnTrainingResult(models.Model):
    patch = models.ForeignKey(Patch, on_delete=models.PROTECT, related_name='nn_results')
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    training_matches = models.BigIntegerField()
    testing_matches = models.BigIntegerField()
    training_accuracy = models.FloatField()
    testing_accuracy = models.FloatField()
    radiant_win_test_percentage = models.FloatField()

class PatchStatistics(models.Model):
    patch = models.OneToOneField(Patch, on_delete=models.PROTECT, primary_key=True, related_name="statistics")
    match_quantity = models.BigIntegerField()

class HeroesStatistics(models.Model):
    patch_statistics = models.ForeignKey(PatchStatistics, on_delete=models.PROTECT, related_name='heroes_statistics')
    hero_bundle = models.CharField(validators=[validate_comma_separated_integer_list], max_length=255)
    bundle_size = models.IntegerField(default=1)
    counter_pick = models.BooleanField(default=False)
    pick_rate = models.FloatField(default=0.0)
    win_rate = models.FloatField(default=0.0)
    confidence = models.FloatField(default=0.0)
