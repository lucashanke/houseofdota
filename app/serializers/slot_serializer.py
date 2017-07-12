from rest_framework import serializers
from app.models import Slot


class SlotSerializer(serializers.ModelSerializer):

    class Meta:
        model = Slot
        fields = ('match', 'team', 'hero_id')
