from abc import abstractmethod
from ..models import Item


class BonusBase(object):
    __kwargs = None
    __item_obj = None
    form = None

    def __init__(self, item_obj: Item, **kwargs):
        self.__item_obj = item_obj
        self.__kwargs = kwargs

    def get_item_option(self, option: str):
        options = self.__item_obj.options

        if f'{option}' not in options:
            raise Exception(f'Nie znaleziono opcji {option}')

        return options.get(option)

    @abstractmethod
    def after_bought(self, **kwargs):
        pass
