from rest_framework import serializers
from rest_framework.serializers import ModelSerializer

from utils.models import Unit


class UnitSerializer(ModelSerializer):
    def empty(self, *args):
        return ""

    class Meta:
        model = Unit
        fields = '__all__'
