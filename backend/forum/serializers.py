from rest_framework import serializers
from .models import Category, Thread, Post
from accounts.serializers import AccountSerializer


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = [
            'id',
            'name'
        ]


class ThreadSerializer(serializers.ModelSerializer):
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
        read_only_fields = ('status', 'pinned', 'created', 'updated')


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
        read_only_fields = ('created', 'updated')

    def create(self, validated_data):
        thread = validated_data['thread']

        if not thread.status == Thread.ThreadStatusChoices.OPENED:
            raise serializers.ValidationError(detail='Temat w którym próbujesz napisać post jest ukryty lub zamknięty',
                                              code=400)

        return Post.objects.create(**validated_data)