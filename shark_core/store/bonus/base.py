from abc import ABC, abstractmethod
import json
from django.contrib.auth.models import Group
from django.contrib.auth import get_user_model


class BaseBonus(ABC):
    TAG = ''

    def __init__(self, model_instance):
        self.model_instance = model_instance

    @staticmethod
    def get_user_by_id(user_id):
        user = get_user_model()
        return user.objects.get(pk=user_id)

    @staticmethod
    def get_group_by_id(group_id):
        return Group.objects.get(pk=group_id)

    @abstractmethod
    def add_bonus(self):
        pass
