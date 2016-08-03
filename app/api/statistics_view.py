from rest_framework.response import Response
from rest_framework.decorators import api_view

from app.services.statistics_service import StatisticsService
from app.serializers.statistics_serializer import HeroesStatisticsSerializer

@api_view()
def heroes_statistics(request):
    heroes_statistics = StatisticsService(quantity=1000).get_heroes_statistics()
    serializer = HeroesStatisticsSerializer(heroes_statistics)
    return Response(serializer.data)
