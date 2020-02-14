from rest_framework import views, generics, status
from rest_framework.permissions import (
    IsAuthenticated,
    AllowAny
)
from rest_framework.response import Response
from rest_framework_simplejwt.views import TokenObtainPairView

from oauth2_provider.contrib.rest_framework import OAuth2Authentication, TokenHasReadWriteScope

from .serializers import (
    AccountSerializer,
    AccountMeSerializer,
    SteamTokenObtainSerializer,
    ServerSteamTokenObtainSerializer,
    RoleSerializer,
    AccountMeUpdateDisplayRoleSerializer,
    AccountMeWalletListSerializer
)
from .models import (
    Account,
    Role,
    Wallet
)
from .mixins import (
    AccountThreadsPostCounterMixin
)

"""
Przypisujemy permisje do stalych
"""
# Dostep dla wszystkich
PERM_ALLOW_ANY = AllowAny
# Dostep tylko dla zalogowanych
PERM_IS_AUTHENTICATED = IsAuthenticated


class AccountListView(generics.ListAPIView, AccountThreadsPostCounterMixin):
    """
    Widok listy uzytkowników
    """

    permission_classes = (PERM_ALLOW_ANY,)
    serializer_class = AccountSerializer
    filterset_fields = ['is_active', 'display_role']
    ordering = ['-id']

    def get_queryset(self):
        return Account.objects.get_queryset().order_by('id')

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        # Formatujemy queryset
        formatted_queryset = self.format_queryset(queryset, many=True)
        page = self.paginate_queryset(formatted_queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(formatted_queryset, many=True)
        return Response(serializer.data)


account_list = AccountListView.as_view()


class AccountMeView(generics.RetrieveAPIView, AccountThreadsPostCounterMixin):
    """
    Widok danych zalogowanego uzytkownika
    """
    permission_classes = (PERM_IS_AUTHENTICATED,)
    serializer_class = AccountMeSerializer

    def retrieve(self, request, *args, **kwargs):
        account = request.user
        account = self.format_queryset(account)
        serializer = self.get_serializer(account)
        return Response(serializer.data)


account_me = AccountMeView.as_view()


class AccountMeUpdateDisplayRoleView(generics.UpdateAPIView):
    """
    Widok aktualizacji wyswietlanej roli
    """
    permission_classes = (PERM_IS_AUTHENTICATED,)
    serializer_class = AccountMeUpdateDisplayRoleSerializer

    def update(self, request, *args, **kwargs):
        account = request.user
        serializer = self.get_serializer(account, data=request.data)
        serializer.is_valid(raise_exception=True)
        return self.perform_update(serializer)

    def perform_update(self, serializer):
        role_pk = serializer.validated_data['role']

        try:
            Role.objects.get(pk=role_pk)
        except Role.DoesNotExist:
            return Response(data={'msg': 'Podana rola nie istnieje'}, status=status.HTTP_400_BAD_REQUEST)

        serializer.save()

        return Response(serializer.data)


account_me_update_display_role = AccountMeUpdateDisplayRoleView.as_view()


class AccountMeWalletListView(generics.ListAPIView):
    """
    Widok listy porfeli danego uzytkownika
    """
    permission_classes = (PERM_IS_AUTHENTICATED,)
    serializer_class = AccountMeWalletListSerializer
    filterset_fields = ['wtype',]

    def list(self, request, *args, **kwargs):
        account = request.user
        queryset = self.filter_queryset(account.wallet_set.all().order_by('id'))
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)


account_me_wallet_list = AccountMeWalletListView.as_view()


class AccountAuthSteamTokenView(TokenObtainPairView):
    """
    Tworzy uzytkownika / zwaraca token dostepu
    """
    serializer_class = SteamTokenObtainSerializer


class ServerAccountAuthSteamTokenView(TokenObtainPairView):
    authentication_classes = (OAuth2Authentication,)
    permission_classes = (TokenHasReadWriteScope,)
    serializer_class = ServerSteamTokenObtainSerializer


class RoleListView(generics.ListAPIView):
    """
    Widok listy rol
    """
    queryset = Role.objects.get_queryset().order_by('id')
    permission_classes = (PERM_ALLOW_ANY,)
    serializer_class = RoleSerializer


role_list = RoleListView.as_view()


class RoleDetailView(generics.RetrieveAPIView):
    """
    Widok pojedynczej roli
    """
    queryset = Role.objects.all()
    permission_classes = (PERM_ALLOW_ANY,)
    serializer_class = RoleSerializer


role_detail = RoleDetailView.as_view()
