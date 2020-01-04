from rest_framework import viewsets
from rest_framework.permissions import AllowAny

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
        queryset = Thread.objects.all()
        categories = self.request.query_params.get('categories', None)
        if categories is not None:
            categories_split = categories.split(',')
            print(categories_split)
            queryset = Thread.objects.filter(categories__pk__in=categories_split).distinct()
        return queryset


class ForumPostViewSet(viewsets.ModelViewSet):
    permission_classes = (AllowAny,)
    # queryset = Post.objects.all()
    serializer_class = ForumPostSerializer

    def get_queryset(self):
        queryset = Post.objects.all()
        thread = self.request.query_params.get('thread', None)
        if thread is not None:
            queryset = Post.objects.filter(thread__pk=thread)
        return queryset


class ForumCommentViewSet(viewsets.ModelViewSet):
    permission_classes = (AllowAny,)
    # queryset = Comment.objects.all()
    serializer_class = ForumCommentSerializer
    
    def get_queryset(self):
        queryset = Post.objects.all()
        post = self.request.query_params.get('post', None)
        if post is not None:
            queryset = Comment.objects.filter(post__pk=post)
        return queryset