from rest_framework.response import Response
from rest_framework.decorators import api_view

from app.services.statistics_service import StatisticsService
from app.serializers.statistics_serializer import *
from app.repositories.patch_repository import PatchRepository

@api_view()
def heroes_statistics(request):
    bundle_size = request.query_params.get('bundle_size', 1)
    heroes_statistics = StatisticsService(
        patch=PatchRepository.fetch_current_patch()
    ).get_heroes_statistics_bundles(
        bundle_size=bundle_size
    )
    serializer = BundleAssociationRulesSerializer(heroes_statistics)
    return Response(serializer.data)

@api_view()
def heroes_statistics_for_bundle(request):
    hero_ids = request.query_params.get('hero_ids[]')
    heroes_statistics = StatisticsService(
        patch=PatchRepository.fetch_current_patch()
    ).get_bundle_recommendations(
        hero_ids=[] if hero_ids is None else [str(hero) for hero in hero_ids.split(',')]  ,
    )
    serializer = BundleAssociationRulesSerializer(heroes_statistics)
    return Response(serializer.data)

@api_view()
def counter_pick_statistics(request):
    hero_ids = request.query_params.get('hero_ids[]')
    counter_pick_statistics = {
        'results': StatisticsService(
            patch=PatchRepository.fetch_current_patch()
        ).get_counter_pick_statistics(
            hero_ids=[] if hero_ids is None else [str(hero) for hero in hero_ids.split(',')]  ,
        ),
    }
    serializer = ListCounterPickSerializer(counter_pick_statistics)
    return Response(serializer.data)
