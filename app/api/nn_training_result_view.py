from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from app.serializers.nn_training_result_serializer import NnTrainingResultSerializer
from app.services.nn_training_result_service import NnTrainingResultService
from app.business.patch_business import PatchBusiness

class NnTrainingResultViewset(ModelViewSet):
    queryset = NnTrainingResultService(PatchBusiness.get_current_patch()).get_nn_performance()
    serializer_class = NnTrainingResultSerializer
