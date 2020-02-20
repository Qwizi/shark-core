from django.utils.translation import ugettext_lazy as _
from django.contrib.auth import authenticate
from rest_framework import exceptions, serializers
from rest_framework_simplejwt.tokens import RefreshToken

from .models import (
    Account,
    Role,
    Wallet,
    PaymentMethod,
    BonusCode
)

from .providers import payment_manager

import requests


class RoleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Role
        fields = [
            'id',
            'name',
            'format'
        ]


class RoleUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Role
        fields = [
            'id',
        ]


class AccountSerializer(serializers.ModelSerializer):
    threads = serializers.IntegerField(read_only=True)
    posts = serializers.IntegerField(read_only=True)
    display_role = RoleSerializer()
    roles = RoleSerializer(many=True)
    formatted_username = serializers.CharField(read_only=True)

    class Meta:
        model = Account
        fields = [
            'id',
            'username',
            'formatted_username',
            'steamid64',
            'steamid32',
            'steamid3',
            'display_role',
            'roles',
            'date_joined',
            'threads',
            'posts'
        ]


class AccountMeSerializer(AccountSerializer):
    class Meta:
        model = Account
        fields = [
            'username',
            'formatted_username',
            'steamid64',
            'steamid32',
            'steamid3',
            'display_role',
            'roles',
            'is_active',
            'is_staff',
            'date_joined',
            'threads',
            'posts'
        ]


class AccountMeUpdateDisplayRoleSerializer(serializers.ModelSerializer):
    role = serializers.IntegerField(required=True, write_only=True)

    class Meta:
        model = Account
        fields = [
            'username',
            'display_role',
            'role'
        ]
        read_only_fields = ('username', 'display_role',)
        extra_kwargs = {
            'display_role': {'required': False}
        }

    def update(self, instance, validated_data):
        role = validated_data.get('role')
        role_instance = Role.objects.get(pk=role)
        instance.update_display_role(role_instance)
        return instance


class AccountMeWalletListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Wallet
        fields = '__all__'


class AccountMeWalletExchangeSerializer(serializers.ModelSerializer):
    channel = serializers.ModelField(
        model_field=PaymentMethod()._meta.get_field('name'),
        write_only=True
    )
    code = serializers.CharField(required=True, write_only=True, min_length=8)

    class Meta:
        model = Wallet
        fields = [
            'money',
            'channel',
            'code'
        ]
        read_only_fields = ('money',)

    def validate_channel(self, value):
        """
        Sprawdzamy czy platnoscc jest dostepna dla danego porfela:
        """
        payment_method_exists = self.instance.payment_methods.filter(name=value).exists()

        if not payment_method_exists:
            raise serializers.ValidationError('Portfel nie obsluguje takiej platnosci', 400)
        return value

    def update(self, instance, validated_data):
        channel = validated_data.get('channel')
        code = validated_data.get('code')

        provider_class = None

        # Sprawdzamy czy platnosc jest dostepna dla podanego porfelu

        # payment_method_exists = instance.payment_methods.filter(name=channel).exists()

        # if not payment_method_exists:
        #    raise serializers.ValidationError('Portfel nie obsluguje takiej platnosci', 400)

        if channel == PaymentMethod.PaymentChoices.CODE.value:
            provider_class = payment_manager.bonuscodes.get_provider_class()
        elif channel == PaymentMethod.PaymentChoices.SMS.value:
            provider_class = payment_manager.sms.get_provider_class()
        elif channel == PaymentMethod.PaymentChoices.TRANSFER.value:
            provider_class = payment_manager.transfer.get_provider_class()

        if not provider_class:
            raise serializers.ValidationError('Wewnętrzny blad API', 500)

        provider_instance = provider_class(code=code)

        if not provider_instance.is_valid():
            raise serializers.ValidationError('Podany kod jest niepoprawny', code=400)

        # Pobieramy wartosc pieniedzy do dodania
        money_to_add = provider_instance.get_money()
        # Dodajmy pieniadze do portfela
        instance.add_money(money_to_add)

        return instance


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


class ServerSteamTokenSerializer(serializers.Serializer):
    default_error_messages = {
        'no_active_account': _('No active account found with the given credentials')
    }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['steamid64'] = serializers.CharField()

    def validate(self, attrs):
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


class ServerSteamTokenObtainSerializer(ServerSteamTokenSerializer):
    @classmethod
    def get_token(cls, user):
        return RefreshToken.for_user(user)

    def validate(self, attrs):
        data = super().validate(attrs)

        refresh = self.get_token(self.user)

        data['refresh'] = str(refresh)
        data['access'] = str(refresh.access_token)

        return data


class AdminAccountSerializer(serializers.ModelSerializer):
    class Meta:
        model = Account
        fields = '__all__'
