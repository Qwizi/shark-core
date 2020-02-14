from rest_framework import views, generics
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
    RoleSerializer
)
from .models import (
    Account,
    Role
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
        formatted_queryset = self.create_accounts_querset_with_post_thread_counter(queryset)
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
        account = self.create_account_queryset_with_post_thread_counter(account)
        serializer = self.get_serializer(account)
        return Response(serializer.data)


account_me = AccountMeView.as_view()


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
