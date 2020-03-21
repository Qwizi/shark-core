from rest_framework import (
    status,
    generics
)
from rest_framework.response import Response

from shark_core.permissions import (
    PERM_IS_AUTHENTICATED,
    PERM_ALLOW_ANY
)

from .models import Group, Item, History
from .serializers import (
    ItemSerializer,
    OfferSerializer
)
from .bonuses import bonus_factory


class ItemListView(generics.ListAPIView):
    """
    Widok przedmiotow dostepnych do zakupu
    """
    queryset = Item.objects.all()
    permission_classes = (PERM_ALLOW_ANY,)
    serializer_class = ItemSerializer

    @staticmethod
    def format_queryset(queryset):
        """
        Dodajemy do queryset dodatkowe pola stworzone w danym bonusie
        """
        new_queryset = []

        # Iterujemy po bonusach
        for bonus in queryset:
            # Pobieramy klase bonusu
            bonus_class = bonus_factory.get_bonus(bonus.group.tag)
            # Tworzymy instancje bomusu
            bonus_instance = bonus_class(bonus)
            # Przypisujemy do bonusu dodatwkoe pola
            bonus.fields = bonus_instance.get_fields()
            # Dodajemy do listy
            new_queryset.append(bonus)
        return new_queryset

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        # Formatujemy queryset
        formatted_queryset = self.format_queryset(queryset)
        page = self.paginate_queryset(formatted_queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(formatted_queryset, many=True)
        return Response(serializer.data)


item_list = ItemListView.as_view()


class OfferCreateView(generics.CreateAPIView):
    """
    Widok tworzeniania oferty
    """
    permission_classes = (PERM_IS_AUTHENTICATED,)
    serializer_class = OfferSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            item = serializer.validated_data['item']
            bonus_class = bonus_factory.get_bonus(item.group.tag)
            bonus_instance = bonus_class(item)
            bonus_instance.after_bought(user=request.user,
                                        extra_fields=serializer.validated_data.get('extra_fields', None))

            serializer.save(user=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


offer_create = OfferCreateView.as_view()
