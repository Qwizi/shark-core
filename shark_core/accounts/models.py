from django.db import models
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import AbstractUser, Group


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
