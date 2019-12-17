from django.db import models
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import AbstractUser, Group
from djmoney.models.fields import MoneyField
from djmoney.money import Money
from django.db.models.signals import post_save


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
    money = MoneyField(max_digits=14, decimal_places=2, default_currency='USD', default=0)

    def add_money(self, money):
        money = Money(money, 'USD')
        self.money += money

    def remove_money(self, money):
        money = Money(money, 'USD')
        self.money -= money


def create_account_wallet(sender, **kwargs):
    if kwargs['created']:
        account_wallet = Wallet.objects.create(account=kwargs['instance'])


post_save.connect(create_account_wallet, sender=Account)
