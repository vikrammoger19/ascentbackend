# adminapp/serializers.py
from rest_framework import serializers
from .models import User, Entities

class EntitySerializer(serializers.ModelSerializer):
    class Meta:
        model = Entities
        fields = '__all__'

class AdminSerializer(serializers.ModelSerializer):
    entities = EntitySerializer(many=True, read_only=True)

    class Meta:
        model = User
        fields = '__all__'
