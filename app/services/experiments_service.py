import random
import itertools
from datetime import datetime
from operator import itemgetter

from app.services.statistics_service import StatisticsService

from app.util.dota_util import HEROES_LIST
from app.repositories.patch_repository import PatchRepository
from app.learners.nntrainer import NNTrainer

class ExperimentsService:

    def __init__(self, patch=None):
        patch = PatchRepository.fetch_by_version(patch) or PatchRepository.fetch_current_patch()
        self._statistics_service = StatisticsService(
            patch=patch
        )
        self._nn_trainer = NNTrainer(patch)
        self._patch = patch
        heroes_ids = HEROES_LIST.keys()

    def make_random_experiment(self, allies_criteria='-confidence', counters_criteria='counter_coefficient'):
        seed = datetime.now()
        generator = random.Random(seed)
        allies = []
        enemies = []
        heroes_ids = list(HEROES_LIST.keys())
        team=generator.choice(['radiant','dire'])

        first_pick = generator.choice(self._statistics_service.get_heroes_statistics_bundles(1,
            order_by=allies_criteria
        )['statistics'][:5])['hero_bundle'][0]['id']
        allies.append(first_pick)
        heroes_ids.remove(first_pick)

        while len(enemies) < 5 or len(allies) < 5:
            if len(enemies) < 5:
                enemy = generator.choice(heroes_ids)
                enemies.append(enemy)
                heroes_ids.remove(enemy)

            if len(allies) < 5:
                recommended = []
                recommended_allies = self._statistics_service.get_bundle_recommendations(
                    allies,
                    criteria=allies_criteria
                )
                for recommended_ally in recommended_allies['statistics']:
                    if recommended_ally['recommended'][0]['id'] in heroes_ids:
                        recommended.append(recommended_ally['recommended'][0]['id'])
                        if len(recommended) is 5:
                            break

                if len(recommended) < 10:
                    counters = list(
                        itertools.chain.from_iterable(
                            list(map(lambda counters_for_hero: counters_for_hero['counter_picks'], self._statistics_service.get_counter_pick_statistics(
                                hero_ids=enemies
                            )))
                        )
                    )
                    counters = sorted(counters, key=itemgetter(counters_criteria), reverse=True)
                    for recommended_counter in counters:
                        if recommended_counter['id'] in heroes_ids:
                            recommended.append(recommended_counter['id'])
                            if len(recommended) is 10:
                                break

                ally = generator.choice(recommended)
                allies.append(ally)
                heroes_ids.remove(ally)

        nn_prediction = self._nn_trainer.get_result_for_full_line_up(team, allies, enemies)
        won = (team is 'radiant' and nn_prediction >= 0.5) or (team is 'dire' and nn_prediction <= 0.5)
        print('team: ' + str(team) + ' | allies: ' + str(allies) + ' and enemies: ' + str(enemies) + (' - WON' if won else ' - LOST'))
        return {
            'result': nn_prediction,
            'team': team,
            'won': won,
        }

    def make_random_experiments(self, quantity, allies_criteria = '-confidence', counters_criteria='counter_coefficient'):
        victories = 0
        i = 0
        while i < quantity:
            experiment = self.make_random_experiment(allies_criteria=allies_criteria, counters_criteria=counters_criteria)
            if experiment['won']:
                victories = victories + 1
            i = i + 1
            print(str(i) + 'th partial result:' + str((victories/i)*100) + '%')
        return {
            'result': (victories/quantity)*100,
            'patch': self._patch.version,
            'allies_criteria': allies_criteria,
            'counters_criteria': counters_criteria
        }

    def make_recommender_vs_recommender_experiment(self, allies_criteria='-confidence', counters_criteria='counter_coefficient'):
        seed = datetime.now()
        generator = random.Random(seed)
        allies = []
        enemies = []
        heroes_ids = list(HEROES_LIST.keys())
        team=generator.choice(['radiant','dire'])

        first_pick = generator.choice(self._statistics_service.get_heroes_statistics_bundles(1,
            order_by=allies_criteria
        )['statistics'][:5])['hero_bundle'][0]['id']
        allies.append(first_pick)
        heroes_ids.remove(first_pick)

        while len(enemies) < 5 or len(allies) < 5:
            if len(enemies) < 5:
                recommended = []
                recommended_allies = self._statistics_service.get_bundle_recommendations(
                    enemies,
                    criteria=allies_criteria
                )
                for recommended_ally in recommended_allies['statistics']:
                    if recommended_ally['recommended'][0]['id'] in heroes_ids:
                        recommended.append(recommended_ally['recommended'][0]['id'])
                        if len(recommended) is 5:
                            break

                if len(recommended) < 10:
                    counters = list(
                        itertools.chain.from_iterable(
                            list(map(lambda counters_for_hero: counters_for_hero['counter_picks'], self._statistics_service.get_counter_pick_statistics(
                                hero_ids=allies
                            )))
                        )
                    )
                    counters = sorted(counters, key=itemgetter(counters_criteria), reverse=True)
                    for recommended_counter in counters:
                        if recommended_counter['id'] in heroes_ids:
                            recommended.append(recommended_counter['id'])
                            if len(recommended) is 10:
                                break

                enemy = generator.choice(recommended)
                enemies.append(enemy)
                heroes_ids.remove(enemy)

            if len(allies) < 5:
                recommended = []
                recommended_allies = self._statistics_service.get_bundle_recommendations(
                    allies,
                    criteria=allies_criteria
                )
                for recommended_ally in recommended_allies['statistics']:
                    if recommended_ally['recommended'][0]['id'] in heroes_ids:
                        recommended.append(recommended_ally['recommended'][0]['id'])
                        if len(recommended) is 5:
                            break

                if len(recommended) < 10:
                    counters = list(
                        itertools.chain.from_iterable(
                            list(map(lambda counters_for_hero: counters_for_hero['counter_picks'], self._statistics_service.get_counter_pick_statistics(
                                hero_ids=enemies
                            )))
                        )
                    )
                    counters = sorted(counters, key=itemgetter(counters_criteria), reverse=True)
                    for recommended_counter in counters:
                        if recommended_counter['id'] in heroes_ids:
                            recommended.append(recommended_counter['id'])
                            if len(recommended) is 10:
                                break

                ally = generator.choice(recommended)
                allies.append(ally)
                heroes_ids.remove(ally)

        nn_prediction = self._nn_trainer.get_result_for_full_line_up(team, allies, enemies)
        won = (team is 'radiant' and nn_prediction >= 0.5) or (team is 'dire' and nn_prediction <= 0.5)
        print('team: ' + str(team) + ' | allies: ' + str(allies) + ' and enemies: ' + str(enemies) + (' - WON' if won else ' - LOST'))
        return {
            'result': nn_prediction,
            'team': team,
            'won': won,
        }

    def make_recommender_vs_recommender_experiments(self, quantity, allies_criteria = '-confidence', counters_criteria='counter_coefficient'):
        victories = 0
        i = 0
        while i < quantity:
            experiment = self.make_recommender_vs_recommender_experiment(allies_criteria=allies_criteria, counters_criteria=counters_criteria)
            if experiment['won']:
                victories = victories + 1
            i = i + 1
            print(str(i) + 'th partial result:' + str((victories/i)*100) + '%')
        return {
            'result': (victories/quantity)*100,
            'patch': self._patch.version,
            'allies_criteria': allies_criteria,
            'counters_criteria': counters_criteria
        }
