from rest_framework import serializers

from accounts.serializers import AccountSerializer
from .models import (
    ReactionItem,
    Reaction,
    SubCategory,
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
    user = AccountSerializer(read_only=True)
    item = ReactionItemSerializer(read_only=True)

    class Meta:
        model = Reaction
        fields = [
            'id',
            'user',
            'item'
        ]


class SubCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = SubCategory
        fields = [
            'id',
            'name'
        ]


class CategorySerializer(serializers.ModelSerializer):
    subcategories = SubCategorySerializer(many=True, read_only=True)

    class Meta:
        model = Category
        fields = [
            'id',
            'name',
            'subcategories'
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


class ThreadReactionsSerializer(serializers.Serializer):
    reaction_item = serializers.IntegerField(write_only=True)
    thread = ThreadSerializer(read_only=True)
    reactions = ReactionSerializer(many=True, read_only=True)
    user = AccountSerializer(read_only=True)

    def validate_reaction_item(self, value):
        # Sprawdzamy czy tag reakcji jest poprawny, jezli tak zwracany instancje reakcji
        if not ReactionItem.objects.filter(pk=value).exists():
            raise serializers.ValidationError(detail='Podany tag reakcji jest niepoprawny', code=400)
        return ReactionItem.objects.get(pk=value)

    def create(self, validated_data):
        # Pobieramy instancje thread
        thread = validated_data['thread']
        # Pobieramy instancje reaction item
        reaction_item = validated_data['reaction_item']
        # Pobieramy instance usera
        user = validated_data['user']

        # Sprawdzamy czy uzytkownik juz dodal reakcje do tego tematu jezeli tak zwracamy wyjatek
        if thread.reactions.filter(user=user).exists():
            raise serializers.ValidationError(detail='Nie mozesz dodać ponownie reakcji do tego tematu', code=400)

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
            'best_answer',
            'promotion_answer',
            'reactions'
        ]
        read_only_fields = ('created', 'updated', 'best_answer', 'promotion_answer')

    def create(self, validated_data):
        thread = validated_data['thread']

        if not thread.status == Thread.ThreadStatusChoices.OPENED:
            raise serializers.ValidationError(detail='Temat w którym próbujesz napisać post jest ukryty lub zamknięty',
                                              code=400)

        return Post.objects.create(**validated_data)


class ThreadSetBestAnswerSerializer(serializers.ModelSerializer):
    post = serializers.IntegerField(write_only=True)
    post_set = PostSerializer(read_only=True, many=True)

    class Meta:
        model = Thread
        fields = [
            'post',
            'post_set'
        ]

    def validate_post(self, value):
        if not Post.objects.filter(pk=value).exists():
            raise serializers.ValidationError(detail='Nie znaleziono takiego posta', code=404)
        return value

    def update(self, instance, validated_data):
        # Pobieramy id posta
        post_pk = validated_data['post']

        # Sprawdzamy czy podany post znajduje sie w danym temacie, jezeli nie zwracamy wyjatek
        if not instance.post_set.filter(pk=post_pk).exists():
            raise serializers.ValidationError(detail='Podany post jest nieprawidlowy', code=400)

        # Tworzymy instance posta
        post_instance = instance.post_set.get(pk=post_pk)

        # Ustawiamy post jako najlepsza odpowiedz
        post_instance.set_best_answer()

        # Zwracamy posty w temacie
        return instance


class ThreadUnSetBestAnswerSerializer(ThreadSetBestAnswerSerializer):

    def update(self, instance, validated_data):
        # Pobieramy id posta
        post_pk = validated_data['post']

        # Sprawdzamy czy podany post znajduje sie w danym temacie, jezeli nie zwracamy wyjatek
        if not instance.post_set.filter(pk=post_pk).exists():
            raise serializers.ValidationError(detail='Podany post jest nieprawidlowy', code=400)

        # Tworzymy instance posta
        post_instance = instance.post_set.get(pk=post_pk)

        # Usuwamy z posta najlepsza odpowiedz
        post_instance.unset_best_answer()

        # Zwracamy posty w temacie
        return instance


class StatsSerializer(serializers.Serializer):
    threads = serializers.IntegerField()
    posts = serializers.IntegerField()
