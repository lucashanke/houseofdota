from rest_framework.viewsets import ModelViewSet

from app.serializers.nn_training_result_serializer import NnTrainingResultSerializer
from app.services.nn_training_result_service import NnTrainingResultService
from app.repositories.patch_repository import PatchRepository

class NnTrainingResultViewset(ModelViewSet):
    queryset = NnTrainingResultService(PatchRepository.fetch_current_patch()).get_nn_performance()
    serializer_class = NnTrainingResultSerializer
