from rest_framework import generics

from shark_core.permissions import PERM_ALLOW_ANY
from .models import Event
from .serializers import EventSerializer


class EventListView(generics.ListAPIView):
    """
    Widok listy eventow
    """
    queryset = Event.objects.all().order_by('id')
    serializer_class = EventSerializer
    permission_classes = (PERM_ALLOW_ANY,)


event_list = EventListView.as_view()


class EventDetailView(generics.RetrieveAPIView):
    """
    Widok pojedynczego eventu
    """
    queryset = Event.objects.all().order_by('id')
    serializer_class = EventSerializer
    permission_classes = (PERM_ALLOW_ANY,)


event_detail = EventDetailView.as_view()
