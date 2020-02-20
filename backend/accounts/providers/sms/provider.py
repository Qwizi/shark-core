from abc import (
    ABC,
    abstractmethod
)

from ...models import SMSNumber

import requests


class AbstractSMSProvider(ABC):
    _tag = None
    _api_client = None
    _api_pin = None
    _api_endpoint = None
    _sms_text = None
    _sms_number = None
    _code = None
    _model = SMSNumber
    _instance = None
    _validated = False

    requests = requests

    def __init__(self, code, model=None):
        self._code = code
        if model:
            self._model = model

    @abstractmethod
    def is_valid(self):
        pass

    def get_money(self):
        if self._instance:
            money = self._instance.money

            return money
        return None
