from abc import (
    ABC,
    abstractmethod
)

import requests


class AbstractSMSProvider(ABC):
    _tag = None
    _api_client = None
    _api_pin = None
    _api_endpoint = None
    _sms_text = None
    _sms_number = None
    _code = None
    _model = None
    _instance = None
    _validated = False

    requests = requests

    def __init__(self, model, code):
        self._model = model
        self._code = code

    @abstractmethod
    def validate(self):
        pass

    def get_money(self):

        if self._validated is False:
            raise Exception('Akcja nie zostala zwalidowna')

        if self._instance:
            money = self._instance.money

            return money
