from django.db import models
from django.conf import settings
from django.contrib.postgres.fields import JSONField

from djmoney.models.fields import MoneyField


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
