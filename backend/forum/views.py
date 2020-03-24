from rest_framework import (
    status,
    generics,
    permissions
)
from rest_framework.response import Response

from .models import (
    Category,
    Thread,
    Post,
)

from .serializers import (
    CategorySerializer,
    ThreadSerializer,
    PostSerializer,
    ThreadReactionAddSerializer
)

from shark_core.permissions import (
    PERM_ALLOW_ANY,
    PERM_THREAD,
    PERM_POST,
    PERM_IS_AUTHENTICATED
)


class CategoryListView(generics.ListAPIView):
    """
    Widok listy kategorii
    """
    queryset = Category.objects.get_queryset().order_by('id')
    permission_classes = (PERM_ALLOW_ANY,)
    serializer_class = CategorySerializer


category_list = CategoryListView.as_view()


class CategoryDetailView(generics.RetrieveAPIView):
    """
    Widok pojedynczej kategorii
    """
    queryset = Category.objects.all()
    permission_classes = (permissions.AllowAny,)
    serializer_class = CategorySerializer


category_detail = CategoryDetailView.as_view()


class ThreadListView(generics.ListCreateAPIView):
    """
    Widok tematów
    """
    queryset = Thread.objects.get_queryset().order_by('id')
    permission_classes = (PERM_THREAD,)
    serializer_class = ThreadSerializer
    filterset_fields = ['category', 'status', 'pinned']

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(author=request.user)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


thread_list = ThreadListView.as_view()


class ThreadDetailView(generics.RetrieveAPIView):
    """
    Widok pojedynczego tematu
    """
    queryset = Thread.objects.all()
    permission_classes = (PERM_ALLOW_ANY,)
    serializer_class = ThreadSerializer


thread_detail = ThreadDetailView.as_view()


class ThreadReactionAddView(generics.CreateAPIView):
    """
    Widok dodawania reakcji do tematu
    """
    permission_classes = (PERM_THREAD,)
    serializer_class = ThreadReactionAddSerializer

    def create(self, request, *args, **kwargs):
        thread = Thread.objects.get(pk=kwargs['thread_pk'])
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(user=request.user, thread=thread)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


thread_reaction_add = ThreadReactionAddView.as_view()


class PostListView(generics.ListCreateAPIView):
    """
    Widok listy postow
    """
    queryset = Post.objects.get_queryset().order_by('id')
    permission_classes = (PERM_POST,)
    serializer_class = PostSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(author=request.user)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


post_list = PostListView.as_view()


class PostDetailView(generics.RetrieveAPIView):
    """
    Widok pojedynczego postu
    """
    queryset = Post.objects.all()
    permission_classes = (PERM_ALLOW_ANY,)
    serializer_class = PostSerializer


post_detail = PostDetailView.as_view()
