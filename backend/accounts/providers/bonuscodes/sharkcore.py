from .provider import AbstractBonusCodeProvider


class SharkCoreBonusCodeProvider(AbstractBonusCodeProvider):

    def __init__(self, *args, **kwargs):
        super(SharkCoreBonusCodeProvider, self).__init__(*args, **kwargs)
