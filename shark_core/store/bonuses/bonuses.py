from .base import BaseBonus
from accounts.models import Account


class PremiumBonus(BaseBonus):
    TAG = 'premium'

    def addBonus(self, *args, **kwargs):
        account = Account.objects.get(pk=kwargs['account_id'])
        return account.username
