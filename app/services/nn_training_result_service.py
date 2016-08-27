from app.repositories.nn_training_result_repository import NnTrainingResultRepository
from app.models import Patch

class NnTrainingResultService:

    def get_nn_performance(self):
        return NnTrainingResultRepository.fetch_from_patch(Patch.get_current_patch())
