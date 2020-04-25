from rest_framework import serializers
from .models import News

from accounts.serializers import AccountSerializer


class NewsSerializer(serializers.ModelSerializer):
    author = AccountSerializer(many=False, read_only=True)

    class Meta:
        model = News
        fields = [
            'id',
            'title',
            'slug',
            'content',
            'author',
            'created',
            'updated',
            'visible'
        ]
