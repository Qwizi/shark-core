from django.db import models
from django.conf import settings

from djmoney.models.fields import MoneyField

import json
import string
import random


class Category(models.Model):
    name = models.CharField(max_length=64, unique=True)
    tag = models.CharField(max_length=32, unique=True, null=True)

    def __str__(self):
        return '{}'.format(self.name)


class Type(models.Model):
   # BONUS_CHOICES = bonus_manager.get_bonus_choices()

    tag = models.CharField(
        max_length=32,
        #choices=BONUS_CHOICES,
        #default=BONUS_CHOICES[0][0],
        blank=False,
        unique=True
    )

    def __str__(self):
        return '{}'.format(self.tag)


class Bonus(models.Model):
    name = models.CharField(max_length=64, blank=False, unique=True)
    description = models.TextField(blank=True)
    options = models.TextField(blank=True)
    price = MoneyField(max_digits=14, decimal_places=2, default_currency='PLN', default=0)
    is_active = models.BooleanField(default=True)
    type = models.ForeignKey(Type, on_delete=models.CASCADE, null=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, null=True)

    @staticmethod
    def __is_json(data):
        try:
            dict_data = json.loads(data)
        except ValueError:
            return False
        return True

    def set_options(self, options):
        if self.__is_json(options) is False:
            raise ValueError('Invalid json format')

        self.options = options

    def get_options(self):
        options = json.loads(self.options)
        return options

    def get_module_tag(self):
        return self.module.tag

    def activate(self):
        self.is_active = True

    def deactivate(self):
        self.is_active = False

    def get_split_description(self):
        desc_list = self.description.split('**')
        desc_list.pop(0)

        return desc_list

    def __str__(self):
        return '{} | {} | {}'.format(self.name, self.get_module_tag(), self.category)


class Log(models.Model):
    LOG_STATUS = (
        (1, "Success"),
        (0, 'Failed')
    )

    bonus = models.ForeignKey(Bonus, on_delete=models.CASCADE)
    account = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=16, choices=LOG_STATUS, default=1)

    def __str__(self):
        return '{} | {} | {}'.format(self.bonus.name, self.account.username, self.status)


class Offer(models.Model):
    number = models.CharField(max_length=8, unique=True)
    account = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    bonus = models.ForeignKey(Bonus, on_delete=models.CASCADE)
    wallet_type = models.IntegerField(default=1)

    def __str__(self):
        return '{} | {} | {} '.format(self.number, self.account.username, self.bonus.name)

    @staticmethod
    def __randomize(length=4, uppercase=False):
        if uppercase:
            return ''.join(random.SystemRandom().choice(string.ascii_uppercase + string.digits) for _ in range(length))
        else:
            return ''.join(random.SystemRandom().choice(string.ascii_lowercase + string.digits) for _ in range(length))

    def create_number(self):
        return self.__randomize(length=8, uppercase=True)

    def save(self, *args, **kwargs):
        self.number = self.create_number()
        super(Offer, self).save(*args, **kwargs)
