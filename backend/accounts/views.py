from rest_framework import viewsets, views, generics
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework import status
from rest_framework_simplejwt.views import TokenObtainPairView

from oauth2_provider.contrib.rest_framework import OAuth2Authentication, TokenHasReadWriteScope

from .serializers import (
    AccountSerializer,
    AccountMeSerializer,
    SteamTokenObtainSerializer,
    ServerSteamTokenObtainSerializer
)
from .models import Account


# Lista uzytkownikow
class AccountListView(generics.ListAPIView):
    queryset = Account.objects.all()
    permission_classes = (AllowAny,)
    serializer_class = AccountSerializer

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        page = self.paginate_queryset(queryset)
        if page is not None:
            new_page = []
            for account in page:
                account.threads = account.thread_author_set.all().count()
                account.posts = account.post_author_set.all().count()
                new_page.append(account)

            serializer = self.get_serializer(new_page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)


account_list = AccountListView.as_view()


# Dane zalogowanego uzytkownika
class AccountAuthMeView(views.APIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = AccountMeSerializer

    def get(self, request):
        account = request.user
        serializer = self.serializer_class(account)
        return Response(serializer.data)


account_me = AccountAuthMeView.as_view()


# Tworzy uzytkownika / zwaraca token dostepu
class AccountAuthSteamTokenView(TokenObtainPairView):
    serializer_class = SteamTokenObtainSerializer


class ServerAccountAuthSteamTokenView(TokenObtainPairView):
    authentication_classes = (OAuth2Authentication,)
    permission_classes = (TokenHasReadWriteScope,)
    serializer_class = ServerSteamTokenObtainSerializer
