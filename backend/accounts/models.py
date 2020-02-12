from django.db import models
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import AbstractUser, Group, UserManager
from django.db.models.signals import post_save
from django.conf import settings
from django.db.utils import IntegrityError

from djmoney.models.fields import MoneyField
from djmoney.money import Money

from .steam_helpers import get_steam_user_info


class AccountManager(UserManager):

    def _create_user_steam(self, steamid64, **extra_fields):
        if steamid64 is None:
            raise Exception('Steamid64 cannot be None')

        user_info = get_steam_user_info(steamid64)
        username = extra_fields.pop('username', None)

        if username is not None:
            user_info.pop('username')
            username = self.model.normalize_username(username)
        else:
            username = user_info.pop('username')
            username = self.model.normalize_username(username)

        account = self.model(username=username, **user_info, **extra_fields)

        account.save(using=self._db)

        return account

    def create_user_steam(self, steamid64, **extra_fields):
        extra_fields.setdefault('is_active', True)
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user_steam(steamid64, **extra_fields)

    def create_superuser_steam(self, steamid64, **extra_fields):
        extra_fields.setdefault('is_active', True)
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self._create_user_steam(steamid64, **extra_fields)


class Account(AbstractUser):
    display_group = models.ForeignKey(Group, on_delete=models.CASCADE, null=True)
    bonus_percent = models.IntegerField(default=1)
    last_login = models.DateTimeField(auto_now=True)
    steamid32 = models.CharField(max_length=60, unique=True)
    steamid64 = models.CharField(max_length=60, unique=True)
    steamid3 = models.CharField(max_length=80, null=True, blank=True)
    profileurl = models.CharField(max_length=256, null=True, blank=True)
    avatar = models.CharField(max_length=256, null=True, blank=True)
    avatarmedium = models.CharField(max_length=256, null=True, blank=True)
    avatarfull = models.CharField(max_length=256, null=True, blank=True)
    loccountrycode = models.CharField(max_length=10, null=True, blank=True)

    objects = AccountManager()

    class Meta:
        verbose_name = _('account')
        verbose_name_plural = _('accounts')

    def __str__(self):
        return '{} | {} | {}'.format(self.username, self.steamid64, self.steamid32)

    def activate(self):
        self.is_active = True
        self.save()

    def increase_bonus_percent(self):
        if self.bonus_percent < settings.SHARK_CORE['STORE']['ACCOUNT_MAX_BONUS_PERCENT']:
            self.bonus_percent += 1
            self.save()


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
        users_group, created = Group.objects.get_or_create(pk=3, name='Users')
        account = kwargs['instance']
        account.display_group = users_group
        account.groups.add(users_group)
        account.save()

        Wallet.objects.bulk_create([
            Wallet(wtype=1, account=account),
            Wallet(wtype=2, account=account)
        ])


post_save.connect(on_create_account, sender=Account)
