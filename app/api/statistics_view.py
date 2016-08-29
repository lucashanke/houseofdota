from rest_framework.response import Response
from rest_framework.decorators import api_view

from app.services.statistics_service import StatisticsService
from app.serializers.statistics_serializer import HeroesStatisticsSerializer
from app.repositories.patch_repository import PatchRepository

@api_view()
def heroes_statistics(request):
    heroes_statistics = StatisticsService(PatchRepository.fetch_current_patch()).get_heroes_statistics()
    serializer = HeroesStatisticsSerializer(heroes_statistics)
    return Response(serializer.data)
