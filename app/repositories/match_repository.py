from app.models import Match

class MatchRepository:

    @staticmethod
    def fetch_last_thousand():
        return Match.objects.all().order_by('-start_time')[:1000]

    @staticmethod
    def fetch_all():
        return Match.objects.all().order_by('-start_time')
