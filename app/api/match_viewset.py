from app.serializers.match_serializer import MatchSerializer
from app.repositories.match_repository import MatchRepository

from rest_framework.viewsets import ModelViewSet

class MatchViewset(ModelViewSet):
    queryset = MatchRepository.fetch_all()
    serializer_class = MatchSerializer
