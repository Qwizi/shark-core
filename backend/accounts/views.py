from rest_framework import viewsets, views, generics
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework import status
from rest_framework_simplejwt.views import TokenObtainPairView

from oauth2_provider.contrib.rest_framework import OAuth2Authentication, TokenHasReadWriteScope

from .serializers import AccountSerializer, SteamTokenObtainSerializer, ServerSteamTokenObtainSerializer
from .models import Account


# Lista uzytkownikow
class AccountListView(generics.ListAPIView):
    queryset = Account.objects.all()
    permission_classes = (AllowAny,)
    serializer_class = AccountSerializer


account_list = AccountListView.as_view()


# Dane zalogowanego uzytkownika
class AccountAuthMeView(views.APIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = AccountSerializer

    def get(self, request):
        account = request.user
        serializer = self.serializer_class(account)
        return Response(serializer.data)


account_me = AccountAuthMeView.as_view()


class AccountView(viewsets.ModelViewSet):
    permission_classes = (AllowAny,)
    serializer_class = AccountSerializer

    def get_queryset(self):
        queryset = Account.objects.all()

        is_active = self.request.query_params.get('is_active', None)
        is_staff = self.request.query_params.get('is_staff', None)

        if is_active is not None:
            queryset = Account.objects.filter(is_active=is_active)

        if is_staff is not None:
            queryset = Account.objects.filter(is_staff=is_staff)

        return queryset

    @action(detail=False, methods=['get'], permission_classes=(IsAuthenticated,))
    def me(self, request):
        account = request.user
        serializer = self.serializer_class(account)
        return Response(data=serializer.data, status=status.HTTP_200_OK)


# Tworzy uzytkownika / zwaraca token dostepu
class AccountAuthSteamTokenView(TokenObtainPairView):
    serializer_class = SteamTokenObtainSerializer


class ServerAccountAuthSteamTokenView(TokenObtainPairView):
    authentication_classes = (OAuth2Authentication, )
    permission_classes = (TokenHasReadWriteScope, )
    serializer_class = ServerSteamTokenObtainSerializer
