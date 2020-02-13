from rest_framework import (
    viewsets,
    status,
    generics,
    permissions
)
from rest_framework.response import Response

from .models import (
    Category,
    Thread,
    Post,
    Comment
)

from .serializers import (
    CategorySerializer,
    ThreadSerializer,
    ThreadCreateSerializer,
    PostSerializer,
    PostCreateSerializer,
    CommentSerializer
)

"""
Przypisujemy permisje do stalych
"""
PERM_ALLOW_ANY = permissions.AllowAny
PERM_IS_AUTHENTICATED = permissions.IsAuthenticated


class CategoryListView(generics.ListAPIView):
    """
    Widok listy kategorii
    """
    queryset = Category.objects.all()
    permission_classes = (PERM_ALLOW_ANY,)
    serializer_class = CategorySerializer


forum_category_list = CategoryListView.as_view()


class CategoryDetailView(generics.RetrieveAPIView):
    """
    Widok pojedynczej kategorii
    """
    queryset = Category.objects.all()
    permission_classes = (permissions.AllowAny,)
    serializer_class = CategorySerializer


forum_category_detail = CategoryDetailView.as_view()


class ThreadListView(generics.ListAPIView):
    """
    Widok listy tematow
    """
    queryset = Thread.objects.all()
    permission_classes = (PERM_ALLOW_ANY,)
    serializer_class = ThreadSerializer
    filterset_fields = ['category', 'status', 'pinned']


forum_thread_list = ThreadListView.as_view()


class ThreadCreateView(generics.CreateAPIView):
    """
    Widok tworzenia tematu
    """
    queryset = Thread.objects.all()
    permission_classes = (PERM_IS_AUTHENTICATED,)
    serializer_class = ThreadCreateSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(author=request.user)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


forum_thread_create = ThreadCreateView.as_view()


class ThreadDetailView(generics.RetrieveAPIView):
    """
    Widok pojedynczego tematu
    """
    queryset = Thread.objects.all()
    permission_classes = (PERM_ALLOW_ANY,)
    serializer_class = ThreadSerializer


forum_thread_detail = ThreadDetailView.as_view()


class PostListView(generics.ListAPIView):
    """
    Widok listy postow
    """
    queryset = Post.objects.all()
    permission_classes = (PERM_ALLOW_ANY,)
    serializer_class = PostSerializer


forum_post_list = PostListView.as_view()


class PostDetailView(generics.RetrieveAPIView):
    """
    Widok pojedynczego postu
    """
    queryset = Post.objects.all()
    permission_classes = (PERM_ALLOW_ANY,)
    serializer_class = PostSerializer


forum_post_detail = PostDetailView.as_view()


class PostCreateView(generics.CreateAPIView):
    """
    Widok tworzenia posta
    """

    queryset = Post.objects.all()
    permission_classes = (PERM_IS_AUTHENTICATED,)
    serializer_class = PostCreateSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(author=request.user)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


forum_post_create = PostCreateView.as_view()
