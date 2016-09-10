from app.business.recommendation_business import *

class RecommendationService:

    def __init__(self, patch):
        self._patch = patch

    def get_nn_recommendation(self, team, allies, enemies):
        return {
            'recommendations' : NNRecommendation(self._patch).recommend(team, allies, enemies)
        }
