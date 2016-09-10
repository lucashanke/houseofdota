from rest_framework import serializers

class RecommendationSerializer(serializers.Serializer):
    recommendations = serializers.JSONField()
