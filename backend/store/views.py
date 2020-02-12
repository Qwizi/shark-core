from rest_framework import viewsets, views
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated, AllowAny
from django.conf import settings

from .models import (
    Bonus,
    Category
)
from .serializers import (
    CategorySerializer,
    BonusSerializer,
    StoreOfferSerializer
)


class StoreCategoryViewSet(viewsets.ModelViewSet):
    permission_classes = (AllowAny, )
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class StoreBonusViewSet(viewsets.ModelViewSet):
    permission_classes = (AllowAny,)
    serializer_class = BonusSerializer

    def get_queryset(self):
        queryset = Bonus.objects.all()
        category = self.request.query_params.get('category', None)
        if category is not None:
            if category == '-1':
                queryset = Bonus.objects.all()
            else:
                queryset = Bonus.objects.filter(category__pk=category)

        return queryset


class StoreOfferView(views.APIView):
    permission_classes = (IsAuthenticated, )
    serializer_class = StoreOfferSerializer

    @staticmethod
    def __check_account_wallet(wallet, price):
        if wallet >= price:
            return True
        return False

    @staticmethod
    def __update_account_wallet(**kwargs):
        bonus_after_bought = settings.SHARK_CORE['STORE']['BONUS_AFTER_BOUGHT']
        bonus_after_bought_type = settings.SHARK_CORE['STORE']['BONUS_AFTER_BOUGHT_TYPE'][0]

        current_wallet = kwargs.get('current_wallet', None)
        bonus_price = kwargs.get('bonus_price', None)

        if bonus_after_bought is False:
            current_wallet.remove_money(bonus_price)
            current_wallet.save()
        else:
            if bonus_after_bought_type == 'BonusWallet':
                current_wallet.remove_money(bonus_price)
                current_wallet.save()

                bonus_wallet = kwargs.get('bonus_wallet', None)
                percent_bonus = bonus_wallet.bonus_percent / 100 * bonus_price

                bonus_wallet.add_money(percent_bonus)
                bonus_wallet.increase_bonus_percent()
                bonus_wallet.save()

            elif bonus_after_bought_type == 'BonusAccount':
                account = kwargs.get('account', None)
                price = account.bonus_percent / 100 * bonus_price
                account.increase_bonus_percent()
                account.save()
                current_wallet.remove_money(price)
                current_wallet.save()

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            account = self.request.user
            bonus = serializer.validated_data.get('bonus', None)
            wallet_type = serializer.validated_data.get('wallet_type', None)

            primary_wallet = account.wallet_set.get(wtype=1)
            bonus_wallet = account.wallet_set.get(wtype=2)

            if wallet_type == 1:
                current_wallet = primary_wallet
            elif wallet_type == 2:
                current_wallet = bonus_wallet
            else:
                current_wallet = None

            if self.__check_account_wallet(current_wallet.money, bonus.price) is False:
                return Response(
                    data={
                        'message': 'Uzytkownik nie posiada wymaganych srodkow w portfelu'
                    }
                )

            bonus_class = bonus_manager.get_bonus(bonus.get_module_tag())

            if bonus_class is None:
                return Response(
                    data={
                        'message': 'Cos poszlo nie tak'
                    },
                    status=status.HTTP_400_BAD_REQUEST
                )

            bonus_instance = bonus_class()
            bonus_instance.set_account(account)
            bonus_instance.set_bonus(bonus)
            bonus_instance.execute()

            wallet_data = {
                'current_wallet': current_wallet,
                'bonus_wallet': bonus_wallet,
                'bonus_price': bonus.price,
                'account': account
            }

            self.__update_account_wallet(**wallet_data)

            serializer.save(account=account)

            return Response(data={
                'number': serializer.data['number']
            }, status=status.HTTP_201_CREATED)

        else:
            return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)
