from app.util.dota_util import HEROES_LIST

class HeroesService:

    def get_heroes(self):
        return {
            'heroes': [ {
                'hero_id': hero_id,
                'localized_name': HEROES_LIST[hero_id]['localized_name']
            } for hero_id in HEROES_LIST.keys() ]
        }
