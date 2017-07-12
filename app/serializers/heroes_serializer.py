from rest_framework import serializers


class HeroesSerializer(serializers.Serializer):
    heroes = serializers.JSONField()
