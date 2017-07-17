from rest_framework import serializers
from app.models import WinningBundleStatistics

#pylint: disable=abstract-method
class WinningBundleStatisticsSerializer(serializers.ModelSerializer):
    heroes = serializers.JSONField()

    class Meta:
        model = WinningBundleStatistics
        fields = '__all__'

#pylint: disable=abstract-method
class WinningBundlesStatisticsSerializer(serializers.Serializer):
    match_quantity = serializers.IntegerField()
    patch = serializers.CharField()
    statistics = serializers.ListField(child=WinningBundleStatisticsSerializer())
