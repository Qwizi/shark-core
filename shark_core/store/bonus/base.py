from abc import ABC, abstractmethod


class BaseBonus(ABC):
    TAG = ''

    def __init__(self, model_instance):
        self.model_instance = model_instance

    @abstractmethod
    def addBonus(self):
        pass
