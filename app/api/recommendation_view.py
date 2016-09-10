from rest_framework.response import Response
from rest_framework.decorators import api_view

from app.services.recommendation_service import *
from app.serializers.recommendation_serializer import *
from app.repositories.patch_repository import PatchRepository

@api_view()
def nn_recommendation(request):
    team = request.query_params.get('team', 'radiant')
    allies = request.query_params.get('allies[]')
    enemies = request.query_params.get('enemies[]')
    recomendations = RecommendationService(
        patch=PatchRepository.fetch_current_patch()
    ).get_nn_recommendation(
        team=team,
        allies=[] if allies is None else [int(ally) for ally in allies.split(',')]  ,
        enemies=[] if enemies is None else [int(enemy) for enemy in enemies.split(',')]
    )
    serializer = RecommendationSerializer(recomendations)
    return Response(serializer.data)
