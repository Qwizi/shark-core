from abc import abstractmethod
from ..models import Item


class BonusBase(object):
    __kwargs = None
    __item_obj = None
    __fields = []

    def __init__(self, item_obj: Item, **kwargs):
        self.__item_obj = item_obj
        self.__kwargs = kwargs

    def get_item_obj(self):
        return self.__item_obj

    def get_fields(self):
        return self.__fields

    def get_kwargs(self):
        return self.__kwargs

    def get_option(self, option: str):
        options = self.__item_obj.options

        if f'{option}' not in options:
            raise Exception(f'Nie znaleziono opcji {option}')

        return options.get(option)

    def create_field(self, name, type, **kwargs):
        field_type = type
        field_id = kwargs.get('id', None)
        field_name = name
        field_value = kwargs.get('value', None)
        field_placeholder = kwargs.get('placeholder', None)
        field_choices = kwargs.get('choices', None)

        if 'id' not in kwargs and field_name:
            field_id = f'{field_name}_id'

        field_dict = {
            'type': field_type,
            'id': field_id,
            'name': field_name,
            'value': field_value,
            'placeholder': field_placeholder,
            'choices': field_choices
        }

        return self.__fields.append(field_dict)

    @abstractmethod
    def after_bought(self, **kwargs):
        pass
