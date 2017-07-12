from rest_framework import serializers


class ExperimentSerializer(serializers.Serializer):
    experiment = serializers.FloatField()
