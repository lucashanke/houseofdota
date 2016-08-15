from app.repositories.nn_training_result_repository import NnTrainingResultRepository

class NnTrainingResultService:

    def get_nn_performance(self):
        return NnTrainingResultRepository.fetch_from_patch('6.88b')
