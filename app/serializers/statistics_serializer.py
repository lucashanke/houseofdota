from rest_framework import serializers
from app.models import WinningBundleStatistics
from app.business.statistics_business import get_heroes_from_association

class WinningBundleStatisticsSerializer(serializers.ModelSerializer):
    heroes = serializers.JSONField()
    class Meta:
        model = WinningBundleStatistics
        fields = '__all__'

class BundleAssociationRulesSerializer(serializers.Serializer):
    match_quantity = serializers.IntegerField()
    patch = serializers.CharField()
    statistics = serializers.ListField(child=WinningBundleStatisticsSerializer())
