from app.repositories.nn_training_result_repository import fetch_from_patch

#pylint: disable=too-few-public-methods
class NnTrainingResultService:

    def __init__(self, patch):
        self._patch = patch

    def get_nn_performance(self):
        return fetch_from_patch(self._patch)
