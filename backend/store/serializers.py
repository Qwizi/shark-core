from rest_framework import serializers
from accounts.serializers import AccountSerializer, AccountMeWalletListSerializer

from .models import Item, History


class ItemSerializer(serializers.ModelSerializer):
    fields = serializers.ListField(read_only=True)

    class Meta:
        model = Item
        fields = [
            'id',
            'name',
            'description',
            'price',
            'options',
            'group',
            'fields'
        ]


class OfferItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = Item
        fields = [
            'id',
            'name',
            'description',
            'price',
            'options',
            'group'
        ]


class OfferSerializer(serializers.Serializer):
    user = AccountSerializer(required=False)
    item = serializers.IntegerField(write_only=True, required=True)
    wallet_type = serializers.IntegerField(write_only=True)
    extra_fields = serializers.ListField(required=False)

    def validate_item(self, value):
        return Item.objects.get(pk=value)

    def create(self, validated_data):
        user = validated_data['user']
        item = validated_data['item']
        wallet_type = validated_data.pop('wallet_type')
        extra_fields = validated_data.pop('extra_fields', None)

        # Sprawdzamy czy podany typ portfela jest poprawny
        if not user.wallet_set.filter(wtype=wallet_type).exists():
            raise serializers.ValidationError(detail='Wystapil problem z portfelem', code=500)

        # Pobieramy portfel dla usera
        wallet = user.wallet_set.get(wtype=wallet_type)

        # Jezeli w portfelu brak odpowiednich srodkow zwracamy wyjatek
        if wallet.money < item.price:
            raise serializers.ValidationError(detail='Nie posiadasz środkow w portfelu', code=400)

        # Odjemjujemy pieniadze z porfela
        wallet.subtract_money(item.price)

        # Tworzymy historie
        return History.objects.create(user=user, item=item)
