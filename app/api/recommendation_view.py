from rest_framework.response import Response
from rest_framework.decorators import api_view

from app.services.recommendation_service import RecommendationService
from app.serializers.recommendation_serializer import BundleRecommendationSerializer, \
ListCounterRecommendationSerializer
from app.repositories.patch_repository import PatchRepository

@api_view()
def hero_recommendations_for_bundle(request):
    hero_ids = request.query_params.get('hero_ids[]')
    heroes_statistics = RecommendationService(
        patch=PatchRepository.fetch_current_patch()
    ).get_bundle_recommendations(
        hero_ids=[] if hero_ids is None else [str(hero) for hero in hero_ids.split(',')],
    )
    serializer = BundleRecommendationSerializer(heroes_statistics)
    return Response(serializer.data)

@api_view()
#pylint: disable=invalid-name
def counter_recommendations_for_hero(request):
    hero_ids = request.query_params.get('hero_ids[]')
    counter_pick_statistics = {
        'results': RecommendationService(
            patch=PatchRepository.fetch_current_patch()
        ).get_counter_recommendations(
            hero_ids=[] if hero_ids is None else [str(hero) for hero in hero_ids.split(',')],
        ),
    }
    serializer = ListCounterRecommendationSerializer(counter_pick_statistics)
    return Response(serializer.data)
