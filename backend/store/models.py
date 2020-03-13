from django.db import models
from django.conf import settings
from django.contrib.postgres.fields import JSONField

from djmoney.models.fields import MoneyField

from servers.models import Server

class Group(models.Model):
    tag = models.CharField(max_length=32, unique=True, default='vip')
    name = models.CharField(max_length=64)

    def __str__(self):
        return f'{self.tag} | {self.name}'


class Item(models.Model):
    name = models.CharField(max_length=64)
    description = models.TextField()
    price = MoneyField(max_digits=14, decimal_places=2, default_currency='PLN', default=0)
    options = JSONField()
    group = models.ForeignKey(Group, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.group.tag} | {self.name} | {self.price}'


class History(models.Model):
    date = models.DateTimeField(auto_now=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    item = models.ForeignKey(Item, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.user.username} | {self.item.name}'


class VipCache(models.Model):

    class VipFlagsChoices(models.TextChoices):
        ADMFLAG_RESERVATION = 'a'
        ADMFLAG_GENERIC = 'b'
        ADMFLAG_KICK = 'c'
        ADMFLAG_BAN = 'd'
        ADMFLAG_UNBAN = 'e'
        ADMFLAG_SLAY = 'f'
        ADMFLAG_CHANGEMAP = 'g'
        ADMFLAG_CONVARS = 'h'
        ADMFLAG_CONFIG = 'i'
        ADMFLAG_CHAT = 'j'
        ADMFLAG_VOTE = 'k'
        ADMFLAG_PASSWORD = 'l'
        ADMFLAG_RCON = 'm'
        ADMFLAG_CHEATS = 'n'
        ADMFLAG_ROOT = 'z'
        ADMFLAG_CUSTOM1 = 'o'
        ADMFLAG_CUSTOM2 = 'p'
        ADMFLAG_CUSTOM3 = 'q'
        ADMFLAG_CUSTOM4 = 'r'
        ADMFLAG_CUSTOM5 = 's'
        ADMFLAG_CUSTOM6 = 't'

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    flag = models.CharField(max_length=32, choices=VipFlagsChoices.choices, default=VipFlagsChoices.ADMFLAG_RESERVATION)
    server = models.ForeignKey(Server, on_delete=models.CASCADE, null=True)
    end = models.DateTimeField()
