from .bonus_base import BaseBonus


class PremiumAccountBonus(BaseBonus):
    TAG = 'premium_account'

    def execute(self, *args, **kwargs):
        pass

