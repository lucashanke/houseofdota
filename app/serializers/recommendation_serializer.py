from rest_framework import serializers

#pylint: disable=abstract-method
class CounterRecommendationSerializer(serializers.Serializer):
    match_quantity = serializers.IntegerField()
    counter_picks = serializers.JSONField()


#pylint: disable=abstract-method
class ListCounterRecommendationSerializer(serializers.Serializer):
    results = serializers.ListField(child=CounterRecommendationSerializer())


#pylint: disable=abstract-method
class BundleRecommendationSerializer(serializers.Serializer):
    match_quantity = serializers.IntegerField()
    patch = serializers.CharField()
    statistics = serializers.JSONField()
