from django.db import models

from djmoney.models.fields import MoneyField

from .bonus import bonus_manager
import json


class BonusModule(models.Model):
    BONUS_CHOICES = bonus_manager.get_bonus_choices()

    tag = models.CharField(
        max_length=32,
        choices=BONUS_CHOICES,
        default=BONUS_CHOICES[0][0],
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
    module = models.ForeignKey(BonusModule, on_delete=models.CASCADE, null=True)

    def set_options(self, options):
        self.options = json.dumps(options)

    def get_options(self):
        return json.loads(self.options)

    def get_module_tag(self):
        return self.module.tag

    def activate(self):
        self.is_active = True

    def deactivate(self):
        self.is_active = False

    def __str__(self):
        return '{} - Module ({})'.format(self.name, self.get_module_tag())
