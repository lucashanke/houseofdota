from app.models import Slot

def create_slot_from_json(slot_json, match):
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
