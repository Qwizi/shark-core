from rest_framework import serializers
from .models import Category, Thread, Post, Comment
from accounts.serializers import AccountSerializer


class ForumCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'


class ForumThreadSerializer(serializers.ModelSerializer):
    categories = ForumCategorySerializer(many=True)
    author = AccountSerializer()
    last_poster = AccountSerializer()

    class Meta:
        model = Thread
        fields = '__all__'


class ForumPostSerializer(serializers.ModelSerializer):
    author = AccountSerializer()
    class Meta:
        model = Post
        fields = '__all__'


class ForumCommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = '__all__'
