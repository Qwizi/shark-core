from django.db import models
from django.conf import settings


class Event(models.Model):
    name = models.CharField(max_length=80)
    content = models.TextField()
    rules = models.TextField()
    promoter = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='event_promoter')
    members = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='event_members')
    administrators = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='event_administrators')
    start_date = models.DateTimeField(auto_now_add=True)
    register_date = models.DateTimeField(null=True)
    members_must_register = models.BooleanField(default=False)

    def __str__(self):
        return f'{self.name} | {self.start_date}'
