from rest_framework.response import Response
from rest_framework.decorators import api_view

from app.serializers.heroes_serializer import HeroesSerializer
from app.services.heroes_service import HeroesService

@api_view()
def heroes_list(request):
    serializer = HeroesSerializer(HeroesService().get_heroes())
    return Response(serializer.data)
