from django.db import models
from django.conf import settings
from smadmins.models import Admin

class Game(models.Model):
    tag = models.CharField(max_length=32, unique=True)
    name = models.CharField(max_length=64, unique=True)
    app_id = models.IntegerField(unique=True)

    def __str__(self):
        return '{} - {} ({})'.format(self.tag, self.name, self.app_id)


class Server(models.Model):
    name = models.CharField(max_length=64)
    game = models.ForeignKey(Game, on_delete=models.CASCADE, null=True)
    ip = models.CharField(max_length=64)
    port = models.CharField(max_length=32)
    managers = models.ManyToManyField(settings.AUTH_USER_MODEL)
    admins = models.ManyToManyField(Admin)

    def __str__(self):
        return '{} [{}:{}] ()'.format(self.name, self.ip, self.port, self.game.tag)