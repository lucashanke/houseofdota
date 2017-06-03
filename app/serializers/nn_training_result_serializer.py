from rest_framework import serializers
from app.models import NnTrainingResult

class NnTrainingResultSerializer(serializers.ModelSerializer):

    class Meta:
        model = NnTrainingResult
        fields = '__all__'
