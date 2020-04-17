from django.db import models
from django.conf import settings


class News(models.Model):
    title = models.CharField(max_length=80)
    content = models.TextField()
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now_add=True)
    visible = models.BooleanField(default=True)

    def __str__(self):
        return f'{self.title}  | {self.author.username}'
