from rest_framework import serializers

#pylint: disable=abstract-method
class ExperimentSerializer(serializers.Serializer):
    experiment = serializers.FloatField()
