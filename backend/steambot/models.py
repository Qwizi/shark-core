from django.db import models
from django.conf import settings


class Queue(models.Model):
    account = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    def __str__(self):
        return '{}'.format(self.account.username)
