from django.db import models
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import (
    AbstractUser,
    Group,
    UserManager,
    GroupManager
)
from django.db.models.signals import post_save
from django.conf import settings

from djmoney.models.fields import MoneyField
from djmoney.money import Money

from .steam_helpers import get_steam_user_info
from shark_core.helpers import check_banned_usernames

import random


class AbstractRole(Group):
    class Meta:
        abstract = True


class Role(AbstractRole):
    format = models.CharField(max_length=255, default="{username}")

    @staticmethod
    def _random_number():
        return random.randint(0, 255)

    def _random_color(self):
        return '#%02X%02X%02X' % (self._random_number(), self._random_number(), self._random_number())

    def create_random_color_format(self):
        random_color_format = '<span color="{}">{}</a>'.format(
            self._random_color(),
            self.format
        )
        self.format = random_color_format
        self.save()


class AccountManager(UserManager):

    @staticmethod
    def _get_user_default_role() -> Role:
        """
        Metoda zwracajaca role uzytkownika
        """
        # TODO zamienic na Role.objects.get()
        role, created = Role.objects.get_or_create(
            pk=3,
            name="User",
            format='<span color="rgb(113,118,114)">{username}</span>'
        )
        return role

    @staticmethod
    def _get_user_administrator_role() -> Role:
        """
        Metoda zwracajaca role administratora
        """
        # TODO zamienic na Role.objects.get()
        role, created = Role.objects.get_or_create(
            pk=1,
            name='Admin',
            format='<span color="rgb(242,0,0)">{username}</span>'
        )
        return role

    def _create_user_steam(self, steamid64, **extra_fields):
        if steamid64 is None:
            raise Exception('Steamid64 cannot be None')

        user_info = get_steam_user_info(steamid64)
        username_field = extra_fields.pop('username', None)
        username = user_info.pop('username')

        if username_field is not None:
            username_field = check_banned_usernames(username_field)
            username = self.model.normalize_username(username_field)
        else:
            username = check_banned_usernames(username)
            username = self.model.normalize_username(username)

        account = self.model(username=username, **user_info, **extra_fields)
        account.save(using=self._db)
        account.roles.add(extra_fields.get('display_role'))

        return account

    def create_user_steam(self, steamid64, **extra_fields):
        display_role = self._get_user_default_role()

        extra_fields.setdefault('is_active', True)
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        extra_fields.setdefault('display_role', display_role)
        return self._create_user_steam(steamid64, **extra_fields)

    def create_superuser_steam(self, steamid64, **extra_fields):
        display_role = self._get_user_administrator_role()

        extra_fields.setdefault('is_active', True)
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('display_role', display_role)
        return self._create_user_steam(steamid64, **extra_fields)


class Account(AbstractUser):
    groups = None
    roles = models.ManyToManyField(
        Role,
        verbose_name=_('roles'),
        blank=True,
        help_text=_(
            'The groups this user belongs to. A user will get all permissions '
            'granted to each of their groups.'
        ),
        related_name="account_set",
        related_query_name="account",
    )
    display_role = models.ForeignKey(Role, on_delete=models.CASCADE, null=True, related_name="account_display_role")
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

    def get_formatted_name(self) -> str:
        return self.display_role.format.replace('{username}', self.username)

    def update_display_role(self, role: Role):
        if role in self.roles.all():
            self.display_role = role
        self.save()


class Wallet(models.Model):

    class WalletTypeChoices(models.IntegerChoices):
        PRIMARY = 1
        SECONDARY = 2
        OTHER = 3

    wtype = models.IntegerField(choices=WalletTypeChoices.choices, default=WalletTypeChoices.PRIMARY, null=True)
    account = models.ForeignKey(Account, on_delete=models.CASCADE)
    money = MoneyField(max_digits=14, decimal_places=2, default_currency='PLN', default=0)
    bonus_percent = models.IntegerField(default=5)
    bonus_max = models.IntegerField(default=25)

    def __str__(self):
        return '{} | {}'.format(self.account.username, self.money)

    def add_money(self, money: Money):
        self.money += money
        self.save()

    def subtract_money(self, money: Money):
        self.money -= money
        self.save()


def on_create_account(sender, **kwargs):
    if kwargs['created']:
        account = kwargs['instance']

        Wallet.objects.bulk_create([
            Wallet(wtype=Wallet.WalletTypeChoices.PRIMARY, account=account),
            Wallet(wtype=Wallet.WalletTypeChoices.SECONDARY, account=account)
        ])


post_save.connect(on_create_account, sender=Account)
