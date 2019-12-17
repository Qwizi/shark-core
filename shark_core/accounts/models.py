from django.db import models
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import AbstractUser, Group
from django.db.models.signals import post_save

from djmoney.models.fields import MoneyField
from djmoney.money import Money


class Account(AbstractUser):
    display_group = models.ForeignKey(Group, on_delete=models.CASCADE, null=True)

    class Meta:
        verbose_name = _('account')
        verbose_name_plural = _('accounts')

    def __str__(self):
        return '{} - {} (Active -> {})'.format(self.username, self.email, self.is_activated())

    def activate(self):
        self.is_active = True

    def is_activated(self):
        if self.is_active is True:
            return 'Yes'
        return 'No'


class Wallet(models.Model):
    account = models.ForeignKey(Account, on_delete=models.CASCADE)
    money = MoneyField(max_digits=14, decimal_places=2, default_currency='PLN', default=0)

    def __str__(self):
        return 'Account {} - {}'.format(self.account.username, self.money)

    def add_money(self, money):

        if isinstance(money, Money):
            self.money += money
        else:
            raise TypeError('A money must be Money instance')

    def remove_money(self, money):
        if isinstance(money, Money):
            self.money -= money
        else:
            raise TypeError('A money must be Money instance')


def create_account_wallet(sender, **kwargs):
    if kwargs['created']:
        account_wallet = Wallet.objects.create(account=kwargs['instance'])


post_save.connect(create_account_wallet, sender=Account)
