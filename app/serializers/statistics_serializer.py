from rest_framework import serializers

class HeroesStatisticsSerializer(serializers.Serializer):
    match_quantity = serializers.IntegerField()
    statistics = serializers.JSONField()
