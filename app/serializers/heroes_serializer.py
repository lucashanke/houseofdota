from rest_framework import serializers

#pylint: disable=abstract-method
class HeroesSerializer(serializers.Serializer):
    heroes = serializers.JSONField()
