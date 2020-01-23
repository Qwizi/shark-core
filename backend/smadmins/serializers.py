from rest_framework import serializers

from accounts.models import Account, Steam
from servers.models import Server

from .models import Admin


class AccountSteamAdminSerializer(serializers.ModelSerializer):
    class Meta:
        model = Steam
        fields = [
            'id32'
        ]


class AccountAdminSerializer(serializers.ModelSerializer):
    steam_data = AccountSteamAdminSerializer()

    class Meta:
        model = Account
        fields = [
            'username',
            'steam_data',
        ]


class ServerAdminSerializer(serializers.ModelSerializer):
    class Meta:
        model = Server
        fields = [
            'ip',
            'port'
        ]


class AdminSerializer(serializers.ModelSerializer):
    account = AccountAdminSerializer()
    #servers = ServerAdminSerializer(many=True)

    class Meta:
        model = Admin
        fields = [
            'id',
            'flags',
            'immunity',
            'account',
        #    'servers_set',
            'group'
        ]
