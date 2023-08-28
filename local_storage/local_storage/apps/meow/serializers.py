from rest_framework import serializers

from .models import MeowModel


class MeowSerializer(serializers.ModelSerializer):
    class Meta:
        model = MeowModel
        fields = '__all__'