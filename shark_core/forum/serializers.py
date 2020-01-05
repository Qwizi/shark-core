from rest_framework import serializers
from .models import Category, Thread, Post, Comment
from accounts.serializers import AccountSerializer
from accounts.models import Account


class ForumCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = [
            'id',
            'name'
        ]


class ForumThreadSerializer(serializers.ModelSerializer):
    categories = ForumCategorySerializer(many=True, read_only=True)
    author = AccountSerializer(read_only=True)
    last_poster = AccountSerializer(read_only=True)

    class Meta:
        model = Thread
        fields = [
            'id',
            'title',
            'content',
            'status',
            'author',
            'created',
            'updated',
            'last_poster',
            'categories',
        ]


class ForumPostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = '__all__'


class ForumCommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = '__all__'
