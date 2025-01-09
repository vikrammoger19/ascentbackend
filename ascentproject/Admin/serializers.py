# adminapp/serializers.py
from rest_framework import serializers
from .models import Admin, Entity

class EntitySerializer(serializers.ModelSerializer):
    class Meta:
        model = Entity
        fields = '__all__'

class AdminSerializer(serializers.ModelSerializer):
    entities = EntitySerializer(many=True, read_only=True)

    class Meta:
        model = Admin
        fields = '__all__'
