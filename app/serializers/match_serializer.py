from rest_framework import serializers
from app.serializers.slot_serializer import SlotSerializer
from app.models import Match

class MatchSerializer(serializers.ModelSerializer):
    slots = SlotSerializer(many=True, read_only=True)

    class Meta:
        model = Match
        fields = ('match_id','match_seq_num','radiant_win','duration','start_time','patch','tower_status_radiant','tower_status_dire','barracks_status_radiant','barracks_status_dire','cluster','first_blood_time','lobby_type','human_players','leagueid','game_mode','flags','engine','radiant_score','dire_score','slots')
