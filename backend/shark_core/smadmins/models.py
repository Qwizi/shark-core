from django.db import models
from django.conf import settings
from accounts.models import Group
#from servers.models import Server


class Admin(models.Model):
    account = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    flags = models.CharField(max_length=30, null=True, blank=True)
    immunity = models.PositiveIntegerField(null=True, blank=True)
    group = models.ForeignKey(Group, on_delete=models.CASCADE, null=True, blank=True)
    #server = models.ForeignKey(Server, on_delete=models.CASCADE)

    def __str__(self):
        return '{}'.format(self.account.username)