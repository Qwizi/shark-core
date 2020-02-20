from rest_framework import serializers
from .models import Bonus, Category, Offer
from accounts.models import Wallet


class StoreCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['pk', 'name', 'tag']


class BonusSerializer(serializers.ModelSerializer):
    class Meta:
        model = Bonus
        fields = '__all__'


class StoreOfferSerializer(serializers.ModelSerializer):
    wallet_type = serializers.ChoiceField(choices=Wallet.WalletTypeChoices.choices)

    class Meta:
        model = Offer
        fields = ['number', 'wallet_type', 'bonus']
        read_only_fields = ('number',)
