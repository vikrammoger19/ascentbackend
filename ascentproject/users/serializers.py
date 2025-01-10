from rest_framework import serializers
from .models import Organization,User

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '_all_'  # Include all fields in the response

class EntitiesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Entities
        fields = '_all_'

class OrganizationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Organization
        fields = '_all_'

class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = '_all_'