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
from .permissions import IsAuthenticatedOnCreateUpdate


class ForumCategoryViewSet(viewsets.ModelViewSet):
    permission_classes = (AllowAny,)
    queryset = Category.objects.all()
    serializer_class = ForumCategorySerializer


class ForumThreadViewSet(viewsets.ModelViewSet):
    permission_classes = (IsAuthenticatedOnCreateUpdate,)
    serializer_class = ForumThreadSerializer

    def get_queryset(self):
        queryset = Thread.objects.all().order_by('-created')
        category = self.request.query_params.get('categories', None)
        author = self.request.query_params.get('author', None)
        pinned = self.request.query_params.get('pinned', None)

        if category is not None:
            queryset = Thread.objects.filter(category__pk=category).distinct().order_by('-created')

        if author is not None:
            queryset = Thread.objects.filter(author=author).distinct().order_by(
                '-created')

        if pinned is not None:
            queryset = Thread.objects.filter(pinned=True).distinct().order_by(
                '-created')

        if category is not None and author is not None:
            queryset = Thread.objects.filter(category__pk=category, author=author).distinct().order_by(
                '-created')
        return queryset

    def create(self, request, *args, **kwargs):
        category_id = request.data.get('category', None)
        category = Category.objects.get(id=category_id)

        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(author=self.request.user, category=category)

        return Response(data=serializer.data, status=status.HTTP_201_CREATED)

    def update(self, request, *args, **kwargs):
        instance = self.get_object()

        category_id = request.data.get('category', None)

        if category_id is not None:
            category = Category.objects.get(id=category_id)
            instance.category = category

        instance.author = self.request.user
        instance.save()

        serializer = self.get_serializer(instance, data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        return Response(serializer.data)


class ForumPostViewSet(viewsets.ModelViewSet):
    permission_classes = (IsAuthenticatedOnCreateUpdate,)
    serializer_class = ForumPostSerializer

    def get_queryset(self):
        queryset = Post.objects.all()
        thread = self.request.query_params.get('thread', None)
        if thread is not None:
            queryset = Post.objects.filter(thread__pk=thread)
        return queryset

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(author=self.request.user)

        return Response(data=serializer.data, status=status.HTTP_201_CREATED)


class ForumCommentViewSet(viewsets.ModelViewSet):
    permission_classes = (AllowAny,)
    serializer_class = ForumCommentSerializer

    def get_queryset(self):
        queryset = Comment.objects.all()
        post = self.request.query_params.get('post', None)
        if post is not None:
            queryset = Comment.objects.filter(post__pk=post)
        return queryset