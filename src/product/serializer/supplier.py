from rest_framework.serializers import ModelSerializer
from authentication.models import User


class SupplierSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username']
