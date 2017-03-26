from rest_framework import serializers

class HeroesStatisticsSerializer(serializers.Serializer):
    match_quantity = serializers.IntegerField()
    statistics = serializers.JSONField()

class CounterPickSerializer(serializers.Serializer):
    match_quantity = serializers.IntegerField()
    counter_picks = serializers.JSONField()

class ListCounterPickSerializer(serializers.Serializer):
    results = serializers.ListField(child=CounterPickSerializer())
