from rest_framework import serializers
from .models import Category, Thread, Post, Reaction, ReactionItem
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
            'reactions'
        ]
        read_only_fields = ('status', 'pinned', 'created', 'updated', 'reactions')


class ReactionItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = ReactionItem
        fields = [
            'name',
            'tag',
            'image'
        ]


class ReactionSerializer(serializers.ModelSerializer):
    item = ReactionItemSerializer()

    class Meta:
        model = Reaction
        fields = [
            'item',
            'user'
        ]


class ThreadReactionSerializer(serializers.ModelSerializer):
    item = ReactionItemSerializer(write_only=True)

    class Meta:
        model = Thread
        fields = [
            'reactions',
            'item'
        ]
        read_only_fields = ['reactions']

    def update(self, instance, validated_data):
        reaction = Reaction.objects.create(**validated_data)

        return instance.reactions.add(reaction)


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
            'updated',
            'reactions'
        ]
        read_only_fields = ('created', 'updated', 'reactions')

    def create(self, validated_data):
        thread = validated_data['thread']

        if not thread.status == Thread.ThreadStatusChoices.OPENED:
            raise serializers.ValidationError(detail='Temat w którym próbujesz napisać post jest ukryty lub zamknięty',
                                              code=400)

        return Post.objects.create(**validated_data)


"""

class ThreadReactionSerializer(serializers.Serializer):
    type = serializers.IntegerField()
    thread_pk = serializers.IntegerField()
    item = serializers.IntegerField()
    user = serializers.IntegerField()

    def validate_type(self, value):
        if not value == Reaction.ReactionType.THREAD:
            raise serializers.ValidationError(detail='Bledny typ', code=400)

        return value

    def validate_item(self, value):
        if not ReactionItem.objects.filter(pk=value).exists():
            raise serializers.ValidationError(detail='Taka reakcja nie istnieje', code=400)

        return value

    def validate_thread_pk(self, value):
        if not Thread.objects.filter(pk=value).exists():
            raise serializers.ValidationError(detail='Niepoprawny temat', code=400)

    def create(self, validated_data):
        thread_pk = validated_data.pop('thread_pk')
        thread = Thread.objects.get(thread_pk)

        reaction = Reaction.objects.create(**validated_data)

        return thread.reactions.add(reaction)
"""