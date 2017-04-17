from rest_framework.response import Response
from rest_framework.decorators import api_view

from app.services.experiments_service import ExperimentsService
from app.serializers.experiments_serializer import ExperimentSerializer

@api_view()
def random_experiment(request):
    experiment = ExperimentsService().make_random_experiments()
    serializer = ExperimentSerializer(experiment)
    return Response(serializer.data)
