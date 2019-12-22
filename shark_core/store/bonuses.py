import importlib
from abc import ABC, abstractmethod

from django.conf import settings


class BonusManager(object):
    __bonus_list = None

    def __init__(self):
        self.__bonus_list = self._get_bonus_list_from_settings()

    @staticmethod
    def _get_bonus_list_from_settings():
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
    account_wallet = None
    bonus = None
    options = None
    log_instance = None
    additional_fields = []

    def set_account(self, account):
        from accounts.models import Account
        if isinstance(account, Account):
            self.account = account
            self.account_wallet = self.account.wallet_set.get()
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

    def check_account_wallet(self):
        if self.account_wallet.money >= self.bonus.price:
            return True
        return False

    def update_account_wallet(self):
        self.account_wallet.remove_money(self.bonus.price)
        self.account_wallet.save()

    @abstractmethod
    def add_bonus(self):
        pass

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


class PremiumAccountBonus(BaseBonus):
    TAG = 'premium_account'

    def __init__(self, *args, **kwargs):
        super(PremiumAccountBonus, self).__init__(*args, **kwargs)

        """
            servers_field = {
            'name': 'servers',
            'type': 'CharField',
            'required': True,
        }

        test_field = {
            'name': 'test',
            'type': 'CharField',
            'required': True,
            'widget': 'PasswordInput'
        }

        self.add_additional_form_field(**servers_field)
        self.add_additional_form_field(**test_field)
        """

    def add_bonus(self, *args, **kwargs):
        if self.check_account_wallet():
            self.update_account_wallet()
            self.log_instance.status = 1
            self.log_instance.save()
            return True

        return False
