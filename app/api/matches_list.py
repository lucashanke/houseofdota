from app.models import Match
from app.serializers.match_serializer import MatchSerializer
from app.repositories.match_repository import MatchRepository

from rest_framework.views import APIView
from rest_framework.response import Response

class MatchesList(APIView):
    """
    List 1000 matches
    """
    def get(self, request, format=None):
        matches = MatchRepository.fetch_last_thousand()
        serializer = MatchSerializer(matches, many=True)
        return Response(serializer.data)
