from django.db import models
from accounts.models import Account, Group


class PremiumCache(models.Model):
    account = models.ForeignKey(Account, on_delete=models.CASCADE)
    old_group = models.ForeignKey(Group, on_delete=models.CASCADE, related_name="old_group")
    new_group = models.ForeignKey(Group, on_delete=models.CASCADE, related_name="new_group")
    time = models.DateTimeField()

    def __str__(self):
        return '{} | {} | {} | {}'.format(self.account.username, self.old_group.name, self.new_group.name, self.time)

