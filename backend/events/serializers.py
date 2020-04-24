from rest_framework import serializers

from accounts.serializers import AccountSerializer
from .models import Event


class EventSerializer(serializers.ModelSerializer):
    promoter = AccountSerializer(read_only=True)
    members = AccountSerializer(many=True, read_only=True)
    administrators = AccountSerializer(many=True, read_only=True)

    class Meta:
        model = Event
        fields = [
            'id',
            'name',
            'content',
            'rules',
            'members',
            'administrators',
            'start_date',
            'register_date',
            'members_must_register'
        ]
