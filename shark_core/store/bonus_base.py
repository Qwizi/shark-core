import importlib
from abc import ABC, abstractmethod

from django.conf import settings


class BonusManager(object):
    __bonus_list = None

    def __init__(self):
        self.__bonus_list = self.__get_bonus_list_from_settings()

    @staticmethod
    def __get_bonus_list_from_settings():
        bonus_list = settings.BONUSES
        return bonus_list

    def get_bonus_list(self):
        return self.__bonus_list

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


bonus_manager = BonusManager()


class BaseBonus(ABC):
    TAG = None
    account = None
    bonus = None
    options = None
    log_instance = None
    additional_fields = []

    def set_account(self, account):
        from accounts.models import Account
        if isinstance(account, Account):
            self.account = account
        else:
            raise AttributeError('First argument must be Account Model instance')

    def set_bonus(self, bonus):
        from .models import Bonus
        if isinstance(bonus, Bonus):
            self.bonus = bonus
            self.options = self.bonus.get_options()
        else:
            raise AttributeError('Second argument must be Bonus Model instance')

    def set_log(self, log):
        from .models import Log
        if isinstance(log, Log):
            self.log_instance = log
        else:
            raise AttributeError('Third argument must be Log Model instance')

    def get_additional_form_fields(self):
        return self.additional_fields

    def add_additional_form_field(self, name, type, **kwargs):
        self.additional_fields.append({
            'name': name,
            'type': type,
            'required': kwargs.get('required', None),
            'widget': kwargs.get('widget', None),
            'queryset': kwargs.get('queryset', None),
            'max_length': kwargs.get('max_length', None),
            'min_length': kwargs.get('min_length', None)
        })

    @abstractmethod
    def execute(self):
        pass
