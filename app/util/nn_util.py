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
