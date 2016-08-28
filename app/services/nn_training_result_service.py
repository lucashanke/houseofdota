from app.repositories.nn_training_result_repository import NnTrainingResultRepository
from app.business.patch_business import PatchBusiness

class NnTrainingResultService:

    def get_nn_performance(self):
        return NnTrainingResultRepository.fetch_from_patch(PatchBusiness.get_current_patch())
