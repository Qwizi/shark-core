from store.bonus_base import BaseBonus
from accounts.models import Group


class PremiumAccountBonus(BaseBonus):
    TAG = 'premium_account'

    def execute(self, *args, **kwargs):
        pass
