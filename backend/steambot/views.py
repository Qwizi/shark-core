from rest_framework import (
    generics,
    status
)
from rest_framework.response import Response

from shark_core.permissions import (
    PERM_STEAMBOT_QUEUE
)

from .models import Queue
from .serializers import SteamBotQueueSerializer


class SteamBotQueueListCreateView(generics.ListCreateAPIView):
    """
    Widok kolejki uzytkowników do wymiany z botem
    """
    queryset = Queue.objects.get_queryset().order_by('id')
    permission_classes = (PERM_STEAMBOT_QUEUE,)
    serializer_class = SteamBotQueueSerializer

    def create(self, request, *args, **kwargs):
        account = request.user
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(account=account)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


steambot_queue = SteamBotQueueListCreateView.as_view()
