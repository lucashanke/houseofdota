from app.repositories.nn_training_result_repository import NnTrainingResultRepository


class NnTrainingResultService:

    def __init__(self, patch):
        self._patch = patch

    def get_nn_performance(self):
        return NnTrainingResultRepository.fetch_from_patch(self._patch)
