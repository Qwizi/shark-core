from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework import status
from django.http import HttpResponseRedirect

from .serializers import AccountSerializer
from .models import Account


class AccountViewSet(viewsets.ModelViewSet):
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

    @action(detail=False, methods=['get'])
    def steam_redirect(self, request):
        ABSOLUTE_URL = 'http://localhost:8000/api/v1/accounts/'
        STEAM_LOGIN_URL = 'https://steamcommunity.com/openid/login'

        params = {
            "openid.ns": "http://specs.openid.net/auth/2.0",
            "openid.mode": "checkid_setup",
            "openid.return_to": ABSOLUTE_URL,
            "openid.realm": 'ABSOLUTE_URL',
            "openid.identity": "http://specs.openid.net/auth/2.0/identifier_select",
            "openid.claimed_id": "http://specs.openid.net/auth/2.0/identifier_select"
        }

        response = HttpResponseRedirect()
        response['Content-Type'] = 'application/x-www-form-urlencoded'
        return response

    @action(detail=False, methods=['get'])
    def test_redirect(self, request):
        return HttpResponseRedirect('http://localhost:8000/api/v1/accounts/test_callback/?id=123')

    @action(detail=False, methods=['get'])
    def test_callback(self, request):
        return Response({'id': request.GET.get('id')})

