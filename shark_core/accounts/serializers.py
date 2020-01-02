from abc import ABC

from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainSerializer, RefreshToken
from .models import Account
from djoser.serializers import UserSerializer



class AccountSerializer(UserSerializer):
    class Meta:
        model = Account
        fields = [
            'pk',
            'username',
            'email',
            'display_group',
            'is_active',
            'is_staff',
            'date_joined'
        ]
