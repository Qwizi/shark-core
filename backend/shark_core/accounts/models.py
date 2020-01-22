from django.db import models
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import AbstractUser, Group
from django.db.models.signals import post_save
from django.conf import settings

from djmoney.models.fields import MoneyField
from djmoney.money import Money


class Steam(models.Model):
    id32 = models.CharField(max_length=60, unique=True)
    id64 = models.CharField(max_length=60, unique=True)
    id3 = models.CharField(max_length=80, null=True, blank=True)
    player_name = models.CharField(max_length=80)


class Account(AbstractUser):
    display_group = models.ForeignKey(Group, on_delete=models.CASCADE, null=True)
    bonus_percent = models.IntegerField(default=1)
    last_login = models.DateTimeField(auto_now=True)
    steam_data = models.ForeignKey(Steam, on_delete=models.CASCADE, null=True, blank=True)

    class Meta:
        verbose_name = _('account')
        verbose_name_plural = _('accounts')

    def __str__(self):
        return '{} | {} | {}'.format(self.username, self.email, self.is_activated())

    def activate(self):
        self.is_active = True

    def is_activated(self):
        if self.is_active is True:
            return 'Yes'
        return 'No'

    def increase_bonus_percent(self):
        if self.bonus_percent < settings.SHARK_CORE['STORE']['ACCOUNT_MAX_BONUS_PERCENT']:
            self.bonus_percent += 1

    def get_steamid32(self):
        return self.steam_data.id32

    def get_steamid64(self):
        return self.steam_data.id64


class Wallet(models.Model):
    class WalletTypes(models.IntegerChoices):
        PRIMARY = 1
        SECONDARY = 2
        OTHER = 3

    wtype = models.CharField(max_length=64, choices=WalletTypes.choices, default=WalletTypes.choices[0][0], null=True)
    account = models.ForeignKey(Account, on_delete=models.CASCADE)
    money = MoneyField(max_digits=14, decimal_places=2, default_currency='PLN', default=0)
    bonus_percent = models.IntegerField(default=5)
    bonus_max = models.IntegerField(default=25)

    def __str__(self):
        return '{} | {}'.format(self.account.username, self.money)

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

    def increase_bonus_percent(self):
        if self.bonus_percent < self.bonus_max:
            self.bonus_percent += 1


def on_create_account(sender, **kwargs):
    if kwargs['created']:
        users_group, created = Group.objects.get_or_create(pk=3)
        account = kwargs['instance']
        account.display_group = users_group
        account.groups.add(users_group)
        account.save()

        Wallet.objects.bulk_create([
            Wallet(wtype=1, account=account),
            Wallet(wtype=2, account=account)
        ])


post_save.connect(on_create_account, sender=Account)
