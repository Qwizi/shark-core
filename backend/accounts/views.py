from rest_framework import viewsets, views
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework import status
from rest_framework_simplejwt.views import TokenObtainPairView

from .serializers import AccountSerializer, SteamTokenObtainSerializer
from .models import Account


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


class AccountAuthSteamTokenView(TokenObtainPairView):
    serializer_class = SteamTokenObtainSerializer
