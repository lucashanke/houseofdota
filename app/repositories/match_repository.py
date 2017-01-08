from app.models import Match
from django.db import connection

class MatchRepository:

    @staticmethod
    def fetch_latest(quantity=1000):
        return Match.objects.all().order_by('-start_time')[:quantity]

    @staticmethod
    def fetch_all():
        return Match.objects.all().order_by('-start_time')

    @staticmethod
    def fetch_from_patch(patch, max_matches):
        return Match.objects.filter(patch=patch).order_by('-start_time')[:max_matches]

    @staticmethod
    def fetch_not_analysed(patch):
        return Match.objects.filter(patch=patch, analysed=False)

    @staticmethod
    def get_heroes_matches(patch):
        cursor = connection.cursor()

        cursor.execute("select count(s.hero_id), s.hero_id \
            from app_match m inner join app_slot s on s.match_id=m.match_id \
            where m.patch_id like %s group by s.hero_id order by s.hero_id", [patch.version])
        rows_played = cursor.fetchall()

        cursor.execute("select count(s.hero_id), s.hero_id \
            from app_match m inner join app_slot s on s.match_id=m.match_id \
            where m.patch_id like %s and (s.team='dire' and m.radiant_win=false \
            or s.team='radiant' and m.radiant_win=true) group by s.hero_id order by s.hero_id", [patch.version])
        rows_won = cursor.fetchall()

        matches = {}
        for row in rows_played:
            matches[row[1]] = {}
            matches[row[1]]['played'] = row[0]
        for row in rows_won:
            matches[row[1]]['won'] =  row[0]
        return matches
