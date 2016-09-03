from rest_framework.response import Response
from rest_framework.decorators import api_view

from app.services.statistics_service import StatisticsService
from app.serializers.statistics_serializer import HeroesStatisticsSerializer
from app.repositories.patch_repository import PatchRepository

@api_view()
def heroes_statistics(request):
    bundle_size = request.query_params.get('bundle_size', 1)
    heroes_statistics = StatisticsService(
        patch=PatchRepository.fetch_current_patch()
    ).get_heroes_statistics(
        bundle_size=bundle_size
    )
    serializer = HeroesStatisticsSerializer(heroes_statistics)
    return Response(serializer.data)
