from app.models import Match

class MatchRepository:

    @staticmethod
    def fetch_latest(quantity=1000):
        return Match.objects.all().order_by('-start_time')[:quantity]

    @staticmethod
    def fetch_all():
        return Match.objects.all().order_by('-start_time')
