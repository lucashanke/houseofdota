from app.learners.nntrainer import NNTrainer
from app.util.dota_util import HEROES_LIST

class NNRecommendation:
    def __init__(self, patch):
        self._patch = patch
        self._nn_trainer = NNTrainer(patch)

    def recommend(self, team, allies, enemies):
        results = [{
            'hero_id': hero,
            'hero_name': HEROES_LIST[hero]['localized_name'],
            'result': self._nn_trainer.get_result_for_line_up(team, allies, enemies, hero) if self._hero_not_in_line_up(allies, enemies, hero) else 0
        } for hero in HEROES_LIST.keys() ]
        return sorted(results, key=lambda r: r['result'], reverse=True)

    def _hero_not_in_line_up(self, allies, enemies, hero):
        return hero not in allies and hero not in enemies
