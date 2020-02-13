from rest_framework import serializers
from .models import Category, Thread, Post, Comment
from accounts.serializers import AccountSerializer
from accounts.models import Account


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = [
            'id',
            'name'
        ]


class ThreadSerializer(serializers.ModelSerializer):
    category = CategorySerializer(read_only=True)
    author = AccountSerializer(read_only=True)
    last_poster = AccountSerializer(read_only=True)

    class Meta:
        model = Thread
        fields = [
            'id',
            'title',
            'content',
            'status',
            'pinned',
            'author',
            'created',
            'updated',
            'last_poster',
            'category',
        ]


class ThreadCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Thread
        fields = [
            'title',
            'content',
            'author',
            'category',
        ]
        extra_kwargs = {
            'author': {'required': False}
        }


class PostSerializer(serializers.ModelSerializer):
    author = AccountSerializer(read_only=True)

    class Meta:
        model = Post
        fields = [
            'id',
            'content',
            'thread',
            'author',
            'created',
            'updated'
        ]


class PostCreateSerializer(serializers.ModelSerializer):

    class Meta:
        model = Post
        fields = [
            'thread',
            'content',
            'author'
        ]
        extra_kwargs = {
            'author': {'required': False}
        }


class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = '__all__'
