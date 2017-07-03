from rest_framework import serializers

class BundleAssociationRulesSerializer(serializers.Serializer):
    match_quantity = serializers.IntegerField()
    statistics = serializers.JSONField()

class CounterAssociationRulesSerializer(serializers.Serializer):
    match_quantity = serializers.IntegerField()
    counter_picks = serializers.JSONField()

class ListCounterPickSerializer(serializers.Serializer):
    results = serializers.ListField(child=CounterAssociationRulesSerializer())
