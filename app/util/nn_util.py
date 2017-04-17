from app.util.dota_util import NUMBER_OF_HEROES

def get_nn_input(match):
    return convert_slots(match.slots.all())

def convert_slots(slots):
    input = [0] * NUMBER_OF_HEROES
    for slot in slots:
        if slot.team == 'radiant':
            input[slot.hero_id-1] = 1
        else:
            input[slot.hero_id-1] = -1
    return input

def get_nn_output(match):
    return match.radiant_win

def get_nn_input_for_line_up(team, allies, enemies, hero):
    input = [0] * NUMBER_OF_HEROES
    allies_value = 1 if team == 'radiant' else -1
    enemies_value = -allies_value
    for ally in allies:
        input[ally-1] = allies_value
    for enemy in enemies:
        input[enemy-1] = enemies_value
    input[hero-1] = allies_value
    return input

def get_nn_input_for_full_line_up(team, allies, enemies):
    input = [0] * NUMBER_OF_HEROES
    allies_value = 1 if team == 'radiant' else -1
    enemies_value = -allies_value
    for ally in allies:
        input[ally-1] = allies_value
    for enemy in enemies:
        input[enemy-1] = enemies_value
    return input
