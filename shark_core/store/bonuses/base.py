from abc import ABC, abstractmethod
from django.conf import settings
import importlib


class BonusManager(object):
    __bonus_list = None

    def __init__(self):
        self.__bonus_list = self._get_bonus_list_from_settings()

    @staticmethod
    def _get_bonus_list_from_settings():
        bonus_list = settings.BONUSES
        return bonus_list

    def get_bonus_list(self):
        return [bonus for bonus in self.__bonus_list]

    def get_bonus_classes(self):
        module = importlib.import_module('store.bonuses')
        bonus_instance_list = []

        for bonus in self.__bonus_list:
            name = getattr(module, bonus)
            bonus_instance_list.append(name)

        return bonus_instance_list

    def get_bonus(self, tag):
        for bonus in self.get_bonus_classes():
            if bonus.TAG == tag:
                return bonus
        return None

    def get_bonus_choices(self):
        bonus_choices = []
        for bonus in self.get_bonus_classes():
            bonus_tag = bonus.TAG
            bonus_tag_upper = bonus.TAG.upper()
            bonus_tuple = tuple([bonus_tag, bonus_tag_upper])

            bonus_choices.append(bonus_tuple)

        return bonus_choices


class BaseBonus(ABC):
    TAG = ''

    def __init__(self, model_instance):
        self.model_instance = model_instance

    @abstractmethod
    def addBonus(self):
        pass


bonus_manager = BonusManager()
