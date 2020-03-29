from rest_framework import (
    status,
    generics,
    permissions
)
from rest_framework.response import Response
from django.shortcuts import get_object_or_404

from .models import (
    Category,
    Thread,
    Post,
    ReactionItem
)

from .serializers import (
    CategorySerializer,
    ThreadSerializer,
    ThreadReactionsSerializer,
    ThreadSetBestAnswerSerializer,
    ThreadUnSetBestAnswerSerializer,
    PostSerializer,
    StatsSerializer,
    ReactionSerializer,
    ReactionItemSerializer
)

from shark_core.permissions import (
    PERM_ALLOW_ANY,
    PERM_THREAD,
    PERM_POST,
    PERM_IS_AUTHOR,
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


class ThreadDetailView(generics.RetrieveUpdateAPIView):
    """
    Widok pojedynczego tematu
    """
    queryset = Thread.objects.all()
    permission_classes = (PERM_IS_AUTHOR,)
    serializer_class = ThreadSerializer


thread_detail = ThreadDetailView.as_view()


class ThreadReactionsListView(generics.ListCreateAPIView):
    """
    Widok dodawania reakcji do tematu
    """
    permission_classes = (PERM_THREAD,)
    serializer_class = ThreadReactionsSerializer

    def get_queryset(self):
        thread_pk = self.kwargs['thread_pk']
        thread = get_object_or_404(Thread, pk=thread_pk)
        return thread.reactions.all()

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset().order_by('id'))
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = ReactionSerializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = ReactionSerializer(queryset, many=True)
        return Response(serializer.data)

    def create(self, request, *args, **kwargs):
        thread = Thread.objects.get(pk=kwargs['thread_pk'])
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(user=request.user, thread=thread)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


thread_reactions_list = ThreadReactionsListView.as_view()


class ThreadSetBestAnswerView(generics.UpdateAPIView):
    """
    Widok ustawiania dla tematu najlepszej odpowiedzi
    """
    queryset = Thread.objects.all().order_by('id')
    permission_classes = (PERM_IS_AUTHENTICATED,)
    serializer_class = ThreadSetBestAnswerSerializer


thread_set_best_answer = ThreadSetBestAnswerView.as_view()


class ThreadUnSetBestAnswerView(ThreadSetBestAnswerView):
    """
    Widok usuwania z postu najlepszej odpowiedzi
    """
    serializer_class = ThreadUnSetBestAnswerSerializer


thread_unset_best_answer = ThreadUnSetBestAnswerView.as_view()


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


class PostDetailView(generics.RetrieveUpdateAPIView):
    """
    Widok pojedynczego postu
    """
    queryset = Post.objects.all()
    permission_classes = (PERM_IS_AUTHOR,)
    serializer_class = PostSerializer


post_detail = PostDetailView.as_view()


class StatsView(generics.ListAPIView):
    """
    Widok statystyk forum
    """
    permission_classes = (PERM_ALLOW_ANY,)
    serializer_class = StatsSerializer

    def list(self, request, *args, **kwargs):
        queryset = {
            'threads': Thread.objects.all().count(),
            'posts': Post.objects.all().count()
        }
        serializer = self.get_serializer(queryset)
        return Response(serializer.data)


stats_list = StatsView.as_view()


class ReactionListView(generics.ListAPIView):
    """
    Widok reakcji
    """
    queryset = ReactionItem.objects.all().order_by('id')
    permission_classes = (PERM_ALLOW_ANY,)
    serializer_class = ReactionItemSerializer


reaction_list = ReactionListView.as_view()
