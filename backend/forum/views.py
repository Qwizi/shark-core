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
    ThreadReactionSerializer
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


class ThreadReactionAddView(generics.UpdateAPIView):
    """
    Widok dodawania reakcji do tematow
    """
    permission_classes = (PERM_IS_AUTHENTICATED,)
    serializer_class = ThreadReactionSerializer

    def get_object(self):
        return Thread.objects.get(pk=self.kwargs['pk'])

    def update(self, request, *args, **kwargs):
        user = request.user
        thread = self.get_object()
        serializer = self.get_serializer(thread, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(user=user)
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


class ThreadReactionListView(generics.CreateAPIView):
    """
    Widok tworzenia reakcji
    """
    permission_classes = (PERM_IS_AUTHENTICATED,)
    serializer_class = ThreadReactionSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(user=request.user)
        return Response(serializer.data)


thread_reaction_list = ThreadReactionListView.as_view()
