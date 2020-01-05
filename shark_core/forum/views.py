from rest_framework import viewsets, status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

from accounts.models import Account
from .models import (
    Category,
    Thread,
    Post,
    Comment
)
from .serializers import (
    ForumCategorySerializer,
    ForumThreadSerializer,
    ForumPostSerializer,
    ForumCommentSerializer
)


class ForumCategoryViewSet(viewsets.ModelViewSet):
    permission_classes = (AllowAny,)
    queryset = Category.objects.all()
    serializer_class = ForumCategorySerializer


class ForumThreadViewSet(viewsets.ModelViewSet):
    permission_classes = (AllowAny,)
    # queryset = Thread.objects.all()
    serializer_class = ForumThreadSerializer

    def get_queryset(self):
        queryset = Thread.objects.all().order_by('-created')
        categories = self.request.query_params.get('categories', None)
        author = self.request.query_params.get('author', None)
        pinned = self.request.query_params.get('pinned', None)

        if categories is not None:
            categories_split = categories.split(',')
            queryset = Thread.objects.filter(categories__pk__in=categories_split).distinct().order_by('-created')

        if author is not None:
            queryset = Thread.objects.filter(author=author).distinct().order_by(
                '-created')

        if pinned is not None:
            queryset = Thread.objects.filter(pinned=True).distinct().order_by(
                '-created')

        if categories is not None and author is not None:
            categories_split = categories.split(',')

            queryset = Thread.objects.filter(categories__pk__in=categories_split, author=author).distinct().order_by(
                '-created')
        return queryset

    def create(self, request, *args, **kwargs):
        author_id = request.data.get('author')
        author = Account.objects.get(id=author_id)
        categories = request.data.get('categories', None)

        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        instance = serializer.save(author=author)

        if categories is not None:
            for category in categories:
                instance.categories.add(category)

        return Response(data=serializer.data, status=status.HTTP_201_CREATED)


class ForumPostViewSet(viewsets.ModelViewSet):
    permission_classes = (AllowAny,)
    serializer_class = ForumPostSerializer

    def get_queryset(self):
        queryset = Post.objects.all()
        thread = self.request.query_params.get('thread', None)
        if thread is not None:
            queryset = Post.objects.filter(thread__pk=thread)
        return queryset


class ForumCommentViewSet(viewsets.ModelViewSet):
    permission_classes = (AllowAny,)
    serializer_class = ForumCommentSerializer

    def get_queryset(self):
        queryset = Comment.objects.all()
        post = self.request.query_params.get('post', None)
        if post is not None:
            queryset = Comment.objects.filter(post__pk=post)
        return queryset
