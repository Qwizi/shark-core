from rest_framework import serializers
from .models import Category, Thread, Post, Comment
from accounts.serializers import AccountSerializer
from  accounts.models import Account


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
    category_id = serializers.IntegerField(required=True)

    class Meta:
        model = Thread
        fields = [
            'category_id',
            'title',
            'content',
            'author'
        ]

    def create(self, validated_data):
        # Usuwamy z tablicy category_id
        category_id = validated_data.pop('category_id')
        # author = validated_data.pop('author')

        # Tworzymy instancje kategorii z podanego id
        category_instance = Category.objects.get(id=category_id)
        # author_instance = Account.objects.get(id=author)

        # Tworzymy temat
        instance = Thread.objects.create(**validated_data)

        # Dodajemy categorie do instancji tematu
        instance.category = category_instance
        instance.save()
        # instance.author = author_instance

        return instance


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


class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = '__all__'
