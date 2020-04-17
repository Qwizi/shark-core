from rest_framework import generics

from shark_core.permissions import PERM_ALLOW_ANY
from .models import News
from .serializers import NewsSerializer


class NewsListView(generics.ListAPIView):
    """
    Widok listy aktualnosci
    """
    queryset = News.objects.all().order_by('id')
    serializer_class = NewsSerializer
    permission_classes = (PERM_ALLOW_ANY,)


news_list = NewsListView.as_view()


class NewsDetailView(generics.RetrieveAPIView):
    """
    Widok pojedynczego aktualnosci
    """
    queryset = News.objects.all().order_by('id')
    serializer_class = NewsSerializer
    permission_classes = (PERM_ALLOW_ANY,)


news_detail = NewsDetailView.as_view()
