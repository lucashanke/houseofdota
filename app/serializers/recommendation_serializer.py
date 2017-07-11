from rest_framework import serializers

class CounterRecommendationSerializer(serializers.Serializer):
    match_quantity = serializers.IntegerField()
    counter_picks = serializers.JSONField()

class ListCounterRecommendationSerializer(serializers.Serializer):
    results = serializers.ListField(child=CounterRecommendationSerializer())

class BundleRecommendationSerializer(serializers.Serializer):
    match_quantity = serializers.IntegerField()
    patch = serializers.CharField()
    statistics = serializers.JSONField()
