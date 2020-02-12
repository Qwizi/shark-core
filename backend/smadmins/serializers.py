from rest_framework import serializers

from accounts.models import Account
from servers.models import Server

from .models import Admin



class AccountAdminSerializer(serializers.ModelSerializer):

    class Meta:
        model = Account
        fields = [
            'username',
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
