from abc import ABC
from django.contrib.auth import authenticate
from rest_framework import exceptions, serializers
from .models import Account, Group
from djoser.serializers import UserSerializer
from rest_framework_simplejwt.tokens import RefreshToken
from django.utils.translation import ugettext_lazy as _

import requests


class AccountSerializer(UserSerializer):
    class Meta:
        model = Account
        fields = [
            'id',
            'username',
            'steamid64',
            'steamid32',
            'steamid3',
            'display_group',
            'is_active',
            'is_staff',
            'date_joined',
        ]
        read_only_fields = ('is_active', 'date_joined', 'is_staff', 'display_group')


class SteamTokenSerializer(serializers.Serializer):
    default_error_messages = {
        'no_active_account': _('No active account found with the given credentials')
    }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['steamid64'] = serializers.CharField()
        self.fields['openid_assoc_handle'] = serializers.CharField()
        self.fields['openid_claimed_id'] = serializers.CharField()
        self.fields['openid_identity'] = serializers.CharField()
        self.fields['openid_sig'] = serializers.CharField()
        self.fields['openid_signed'] = serializers.CharField()
        self.fields['openid_ns'] = serializers.CharField()
        self.fields['openid_op_endpoint'] = serializers.CharField()
        self.fields['openid_return_to'] = serializers.CharField()
        self.fields['openid_response_nonce'] = serializers.CharField()

    def validate(self, attrs):
        openid_kwargs = {
            'openid.assoc_handle': attrs['openid_assoc_handle'],
            'openid.claimed_id': attrs['openid_claimed_id'],
            'openid.identity': attrs['openid_identity'],
            'openid.sig': attrs['openid_sig'],
            'openid.signed': attrs['openid_signed'],
            'openid.ns': attrs['openid_ns'],
            'openid.op_endpoint': attrs['openid_op_endpoint'],
            'openid.return_to': attrs['openid_return_to'],
            'openid.response_nonce': attrs['openid_response_nonce'],
            'openid.mode': 'check_authentication',
        }
        print(openid_kwargs)
        response = requests.post('https://steamcommunity.com/openid/login', openid_kwargs)

        if response.status_code != 200:
            raise Exception('Authentication failed', 'authentication_failed')

        is_valid = "is_valid:true" in response.text

        if is_valid is False:
            raise Exception('Steam Authentication failed')

        authenticate_kwargs = {
            'steamid64': attrs['steamid64']
        }

        try:
            authenticate_kwargs['request'] = self.context['request']
        except KeyError:
            pass

        self.user = authenticate(**authenticate_kwargs)

        if self.user is None or not self.user.is_active:
            raise exceptions.AuthenticationFailed(
                self.error_messages['no_active_account'],
                'no_active_account',
            )
        return {}

    @classmethod
    def get_token(cls, user):
        raise NotImplementedError('Must implement `get_token` method for `TokenObtainSerializer` subclasses')


class SteamTokenObtainSerializer(SteamTokenSerializer):
    @classmethod
    def get_token(cls, user):
        return RefreshToken.for_user(user)

    def validate(self, attrs):
        data = super().validate(attrs)

        refresh = self.get_token(self.user)

        data['refresh'] = str(refresh)
        data['access'] = str(refresh.access_token)

        return data