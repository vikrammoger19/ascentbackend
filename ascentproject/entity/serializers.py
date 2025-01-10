from rest_framework import serializers
from .models import Organization, Entities


class OrganizationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Organization
        fields = "__all__"  


class EntitySerializer(serializers.ModelSerializer):
    organization = serializers.PrimaryKeyRelatedField(queryset=Organization.objects.all())

    class Meta:
        model = Entities
        fields = "__all__"  


class EntityCreateUpdateSerializer(serializers.ModelSerializer):
    organization = serializers.PrimaryKeyRelatedField(queryset=Organization.objects.all(), required=False)

    class Meta:
        model = Entities
        fields = "__all__" 
    def validate(self, attrs):
        """
        Add custom validation if needed.
        """
      
        return attrs
