from .provider import AbstractBonusCodeProvider


class SharkCoreBonusCodeProvider(AbstractBonusCodeProvider):

    def __init__(self, model, code: str):
        super().__init__(model, code)
