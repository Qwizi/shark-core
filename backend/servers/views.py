from rest_framework import views, viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny

from steam import game_servers as gs
from .models import Server
from .serializers import ServerSerializer, ServerStatusSerializer
from smadmins.serializers import AdminSerializer


class ServerViewSet(viewsets.ModelViewSet):
    queryset = Server.objects.all()
    serializer_class = ServerSerializer
    permission_classes = (AllowAny,)

    @action(detail=True, methods=['get'])
    def status(self, request, pk=None):
        server = self.get_object()

        ip_port = '{}:{}'.format(server.ip, server.port)
        server_address = next(gs.query_master(r'\appid\{}\gameaddr\{}'.format(server.game.app_id, ip_port)))
        server_info = gs.a2s_info(server_address)
        server_data = {
            'name': server_info['name'],
            'ip': ip_port,
            'players': server_info['players'],
            'max_players': server_info['max_players'],
            'map': server_info['map'],
            'game': server.game.tag
        }

        serializer = ServerStatusSerializer(server_data)
        return Response(serializer.data)

    @action(detail=False, methods=['get'])
    def admins(self, request):
        server_ip = request.query_params.get('server_ip', None)
        server_port = request.query_params.get('server_port', None)
        if server_ip and server_port is not None:
            server = Server.objects.get(ip=server_ip, port=server_port)
            queryset = server.admins.all()
            serializer = AdminSerializer(queryset, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response({'msg': 'IP I PORT!'}, status=status.HTTP_400_BAD_REQUEST)



class ServerStatusViewSet(views.APIView):
    def get(self, request, format=None):
        queryset = Server.objects.all()
        servers = []

        for server in queryset:
            ip_port = '{}:{}'.format(server.ip, server.port)
            server_address = next(gs.query_master(r'\appid\{}\gameaddr\{}'.format(server.game.app_id, ip_port)))
            server_info = gs.a2s_info(server_address)

            server_data = {
                'name': server_info['name'],
                'ip': ip_port,
                'players': server_info['players'],
                'max_players': server_info['max_players'],
                'map': server_info['map'],
                'game': server.game.tag
            }
            servers.append(server_data)

        serializer = ServerStatusSerializer(servers, many=True)
        return Response(serializer.data)
