from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from .serializers import AccountSerializer
from .models import Account


class AccountViewSet(viewsets.ModelViewSet):
    permission_classes = (IsAuthenticated, )
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
