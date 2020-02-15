from abc import ABC

from rest_framework.validators import ValidationError
from djmoney.money import Money

from ...models import BonusCode


class AbstractBonusCodeProvider(ABC):
    _model = None
    _code = None
    _instance = None
    _validated = False

    def __init__(self, code: str, model=None):
        self._code = code

        if model is None:
            self._model = BonusCode
        else:
            self._model = model

    def _set_validate(self, value):
        self._validated = value

    def is_valid(self):
        """
        Validujemy poprawnosc providera
        """
        code_exist = self._model.objects.filter(code=self._code).exists()

        if code_exist:
            self._instance = self._model.objects.get(code=self._code)
            return True
        return False

    def get_money(self) -> Money:
        """
        Zwracamy odpowiednia wartosc pieniedzy
        """

        money = self._instance.money

        # Usuwamy kod z bazy
        self._instance.delete()

        return money
