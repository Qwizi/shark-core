from rest_framework import viewsets
from rest_framework.permissions import AllowAny

from .serializers import AdminSerializer
from .models import Admin


class AdminViewSet(viewsets.ModelViewSet):
    serializer_class = AdminSerializer
    permission_classes = (AllowAny,)

    def get_queryset(self):
        queryset = Admin.objects.all()

        server_ip = self.request.query_params.get('server_ip', None)
        server_port = self.request.query_params.get('server_port', None)

        if server_ip and server_port is not None:
            queryset = Admin.objects.filter(server__ip=server_ip, server__port=server_port)

        return queryset
