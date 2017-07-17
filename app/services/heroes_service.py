from app.util.dota_util import HEROES_LIST

def get_heroes():
    return {
        'heroes': [{
            'hero_id': hero_id,
            'localized_name': hero['localized_name']
        } for hero_id, hero in HEROES_LIST.items()]
    }
