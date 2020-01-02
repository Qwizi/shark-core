from rest_framework import viewsets, views
from rest_framework.response import Response
from rest_framework import status

from djmoney.money import Money

from accounts.models import Account
from .models import (
    Bonus,
    Category
)
from .serializers import (
    CategorySerializer,
    BonusSerializer,
    StoreCheckoutSerializer
)
from .bonus_base import bonus_manager


class StoreCategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class StoreBonusViewSet(viewsets.ModelViewSet):
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


class StoreCheckoutView(views.APIView):
    serializer_class = StoreCheckoutSerializer

    @staticmethod
    def __check_account_wallet(wallet, price):
        if wallet >= price:
            return True
        return False

    @staticmethod
    def __update_account_wallet(wallet_instance, price):
        price = Money(price, 'PLN')
        wallet_instance.remove_money(price)
        wallet_instance.save()

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            account_id = serializer.validated_data.get('account', None)
            bonus_id = serializer.validated_data.get('bonus', None)

            account = Account.objects.get(pk=account_id)
            wallet = account.wallet_set.get()
            bonus = Bonus.objects.get(pk=bonus_id)

            if self.__check_account_wallet(wallet.money, bonus.price):
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

                self.__update_account_wallet(wallet_instance=wallet, price=bonus.price)

                serializer.save()

                return Response(data=serializer.data, status=status.HTTP_201_CREATED)
            else:
                return Response(
                    data={
                        'message': 'Uzytkownik nie posiada wymaganych srodkow w portfelu'
                    }, status=status.HTTP_400_BAD_REQUEST
                )
        else:
            print(serializer.data)
            return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)
