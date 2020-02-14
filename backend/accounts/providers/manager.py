from shark_core.helpers import get_shark_core_settings
from .bonuscodes.provider import AbstractBonusCodeProvider

from abc import (
    ABC,
    abstractmethod
)

import importlib


class AbstractPaymentManager(ABC):
    _provider_class = None

    def __init__(self):
        self._provider_class = self._get_provider_from_settings()

    @staticmethod
    def _create_provider_class(from_setting_provider: str):
        """
        Metoda tworzaca klase providera pobranego z ustawien
        :param from_setting_provider:
        :return:
        """

        """
        Pobieramy nazwe klasy providera
        Wyglada teraz tak
        SharkCoreBonusProvider
        """
        provider_class_name = from_setting_provider.split('.')[-1]

        """
        Zamieniamy pobranego stringa na tablice
        Tablica wyglada tak
        ['accounts', 'providers', 'bonuscodes', 'sharkcore', 'SharkCoreBonusProvider']
        """
        provider_split = from_setting_provider.split('.')

        """
        Usuwamy ostatnią pozycje z listy
        Tablica wyglada tak
        ['accounts', 'providers', 'bonuscodes', 'sharkcore']
        """
        provider_split.pop(-1)

        """
        Przekszalcamy tablice na stringa
        String wyglada tak
        accounts.providers.bonuscodes.sharkcore
        """
        provider_join = '.'.join(provider_split)

        """
        Importujemy modul
        """
        provider_module = importlib.import_module(provider_join)

        """
        Pobieramy klase
        """
        provider_class = getattr(provider_module, provider_class_name)

        return provider_class

    def get_provider_class(self):
        return self._provider_class

    @abstractmethod
    def _get_provider_from_settings(self):
        pass


class BonusCodePaymentManager(AbstractPaymentManager):

    def _get_provider_from_settings(self):
        providers_setting = get_shark_core_settings('PAYMENT_PROVIDERS')
        provider_bonus_code_class = providers_setting.get('BONUS_CODE')['DEFAULT_PROVIDER']

        provider_class = self._create_provider_class(provider_bonus_code_class)

        return provider_class


class SMSPaymentManager(AbstractPaymentManager):

    def _get_provider_from_settings(self):
        providers_setting = get_shark_core_settings('PAYMENT_PROVIDERS')
        provider_sms_class = providers_setting.get('SMS')['DEFAULT_PROVIDER']

        provider_class = self._create_provider_class(provider_sms_class)

        return provider_class


class TransferPaymentManager(AbstractPaymentManager):
    def _get_provider_from_settings(self):
        providers_setting = get_shark_core_settings('PAYMENT_PROVIDERS')
        provider_transfer_class = providers_setting.get('TRANSFER')['DEFAULT_PROVIDER']

        provider_class = self._create_provider_class(provider_transfer_class)

        return provider_class


class PaymentManager(object):
    """
    Menadzer platnosci
    """
    bonuscodes = BonusCodePaymentManager()
    sms = SMSPaymentManager()
    transfer = TransferPaymentManager()


payment_manager = PaymentManager()
