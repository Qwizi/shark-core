from rest_framework import serializers

from .models import Queue
from accounts.models import Account


class SteamBotQueueAccountSerializer(serializers.ModelSerializer):
    class Meta:
        model = Account
        fields = [
            'steamid64',
            'tradeurl'
        ]


class SteamBotQueueSerializer(serializers.ModelSerializer):
    account = SteamBotQueueAccountSerializer(read_only=True)

    class Meta:
        model = Queue
        fields = [
            'account'
        ]

    def create(self, validated_data):
        account = validated_data.get('account')

        if account.tradeurl is None:
            raise serializers.ValidationError(detail='Musisz uzupelnic trade url', code=400)

        return Queue.objects.create(account=account)
