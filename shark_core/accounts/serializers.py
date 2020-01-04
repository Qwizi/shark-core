from abc import ABC

from rest_framework import serializers
from .models import Account, Group
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
            'date_joined',
            'password'
        ]
        read_only_fields = ('is_active', 'date_joined', 'is_staff', 'display_group')
        extra_kwargs = {
            'password': {'write_only': True}
        }

    def create(self, validated_data):
        account = Account.objects.create_user(username=validated_data['username'], email=validated_data['email'],
                                              password=validated_data['password'])

        return validated_data
