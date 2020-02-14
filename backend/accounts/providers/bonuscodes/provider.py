from abc import ABC

from djmoney.money import Money


class AbstractBonusCodeProvider(ABC):
    _model = None
    _code = None
    _instance = None

    def __init__(self, model, code: str):
        self._model = model
        self._code = code

    def validate(self):
        """
        Sprawdzamy czy podany kod istnieje w bazie
        """
        try:
            self._instance = self._model.objects.get(code=self._code)
        except self._model.DoesNotExist:
            return False
        return True

    def get_money(self) -> Money:
        """
        Zwracamy odpowiednia wartosc pieniedzy
        """
        money = self._instance.money

        # Usuwamy kod z bazy
        self._instance.delete()

        return money
