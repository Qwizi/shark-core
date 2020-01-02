from abc import ABC

from rest_framework import serializers
from .models import Server


class ServerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Server
        fields = '__all__'


class ServerStatusSerializer(serializers.Serializer):
    name = serializers.CharField(max_length=64)
    ip = serializers.CharField(max_length=80)
    players = serializers.IntegerField()
    max_players = serializers.IntegerField()
    map = serializers.CharField(max_length=64)
    game = serializers.CharField(max_length=32)
