import random

from app.services.statistics_service import StatisticsService

from app.util.dota_util import HEROES_LIST
from app.repositories.patch_repository import PatchRepository
from app.learners.nntrainer import NNTrainer


class ExperimentsService:

    def __init__(self):
        self._statistics_service = StatisticsService(
            patch=PatchRepository.fetch_current_patch()
        )
        self._nn_trainer = NNTrainer(PatchRepository.fetch_current_patch())
        heroes_ids = HEROES_LIST.keys()

    def make_random_experiment(self):
        allies = []
        enemies = []
        heroes_ids = list(HEROES_LIST.keys())
        team=random.choice(['radiant','dire'])

        first_pick = self._statistics_service.get_heroes_statistics(
            bundle_size=1
        )['statistics'][0]['hero_bundle'][0]['id']
        allies.append(first_pick)
        heroes_ids.remove(first_pick)

        while len(enemies) < 5 or len(allies) < 5:
            print(allies)
            print(enemies)
            if len(enemies) < 5:
                enemy = random.choice(heroes_ids)
                enemies.append(enemy)
                heroes_ids.remove(enemy)


            if len(allies) < 5:
                recommended = self._statistics_service.get_heroes_statistics_recommendation(
                    hero_ids=allies
                )
                if len(recommended['statistics']) > 0:
                    recommended_ally = recommended['statistics'][0]['recommended'][0]['id']

                counters = self._statistics_service.get_counter_pick_statistics(
                    hero_ids=enemies
                )
                if len(counters) > 0:
                    recommended_counter = counters[0]['counter_picks'][0]['hero_id']

                ally = random.choice([recommended_ally, recommended_counter])
                allies.append(ally)
                heroes_ids.remove(ally)

        nn_prediction = self._nn_trainer.get_result_for_full_line_up(team, allies, enemies)
        return {
            'experiment': {
                'result': nn_prediction,
                'winner': team == 'radiant' and nn_prediction >= 0.5
            }
        }
