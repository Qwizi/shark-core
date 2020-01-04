from rest_framework import serializers
from .models import Bonus, Category, Offer
from accounts.models import Wallet


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['pk', 'name', 'tag']


class BonusSerializer(serializers.ModelSerializer):
    class Meta:
        model = Bonus
        fields = '__all__'


class StoreCheckoutSerializer(serializers.ModelSerializer):
    wallet_type = serializers.ChoiceField(choices=Wallet.WalletTypes.choices)

    class Meta:
        model = Offer
        fields = ['number', 'wallet_type', 'account', 'bonus']
        read_only_fields = ('number',)
