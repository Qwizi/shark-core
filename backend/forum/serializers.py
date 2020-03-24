from rest_framework import serializers

from accounts.serializers import AccountSerializer
from .models import (
    ReactionItem,
    Reaction,
    Category,
    Thread,
    Post
)


class ReactionItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = ReactionItem
        fields = [
            'id',
            'name',
            'tag',
            'image'
        ]


class ReactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Reaction
        fields = [
            'id',
            'user',
            'reaction'
        ]


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
    reactions = ReactionItemSerializer(many=True, read_only=True)

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
        read_only_fields = ('status', 'pinned', 'created', 'updated')


class ThreadReactionAddSerializer(serializers.Serializer):
    reaction_tag = serializers.ModelField(ReactionItem()._meta.get_field('tag'), write_only=True)
    thread = ThreadSerializer(read_only=True)
    reactions = ReactionSerializer(many=True, read_only=True)
    user = AccountSerializer(read_only=True)

    def validate_reaction_tag(self, value):
        # Sprawdzamy czy tag reakcji jest poprawny, jezli tak zwracany instancje reakcji
        if not ReactionItem.objects.filter(tag=value).exists():
            serializers.ValidationError('Podany tag reakcji jest niepoprawny')
        return ReactionItem.objects.get(tag=value)

    def create(self, validated_data):
        # Pobieramy instancje thread
        thread = validated_data['thread']
        # Pobieramy instancje reaction item
        reaction_item = validated_data['reaction_tag']
        # Pobieramy instance usera
        user = validated_data['user']

        # Tworzymy reakcje dla tematu
        reaction_instance = Reaction.objects.create(
            user=user,
            item=reaction_item
        )

        # Dodajemy utworzoną reakcje do tematu
        thread.reactions.add(reaction_instance)

        # Zwracamy instancje thread
        return thread.reactions


class PostSerializer(serializers.ModelSerializer):
    author = AccountSerializer(read_only=True)
    reactions = ReactionItemSerializer(many=True, read_only=True)

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
        read_only_fields = ('created', 'updated')

    def create(self, validated_data):
        thread = validated_data['thread']

        if not thread.status == Thread.ThreadStatusChoices.OPENED:
            raise serializers.ValidationError(detail='Temat w którym próbujesz napisać post jest ukryty lub zamknięty',
                                              code=400)

        return Post.objects.create(**validated_data)



class StatsSerializer(serializers.Serializer):
    threads = serializers.IntegerField()
    posts = serializers.IntegerField()
