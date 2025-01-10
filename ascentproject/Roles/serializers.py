# serializers.py
from rest_framework import serializers
from .models import Role, Product

class RoleSerializer(serializers.ModelSerializer):
    product = serializers.PrimaryKeyRelatedField(queryset=Product.objects.all())

    class Meta:
        model = Role
        fields = ['role_id', 'role_name', 'product']
