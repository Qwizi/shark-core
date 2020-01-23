from django.db import models
from accounts.models import Account


class Category(models.Model):
    name = models.CharField(max_length=64, unique=True)

    def __str__(self):
        return '{}'.format(self.name)


class Thread(models.Model):
    class ThreadStatusChoices(models.IntegerChoices):
        CLOSED = 0
        OPENED = 1
        DELETED = 2

    title = models.CharField(max_length=80)
    content = models.TextField()
    category = models.ForeignKey(Category, on_delete=models.CASCADE, null=True)
    author = models.ForeignKey(Account, on_delete=models.CASCADE, related_name='author')
    last_poster = models.ForeignKey(Account, on_delete=models.CASCADE, related_name='last_poster', null=True)
    status = models.IntegerField(choices=ThreadStatusChoices.choices, default=ThreadStatusChoices.OPENED)
    pinned = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return '{} | {} | {}'.format(self.title, self.author.username, self.status)


class Post(models.Model):
    thread = models.ForeignKey(Thread, on_delete=models.CASCADE)
    author = models.ForeignKey(Account, on_delete=models.CASCADE)
    content = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return '{} | {} | {}'.format(self.pk, self.thread.title, self.author.username)

    @staticmethod
    def decode_content(content):
        return content.replace('&', '&amp')

    def save(self, *args, **kwargs):
        self.content = self.decode_content(self.content)
        super(Post, self).save(*args, **kwargs)


class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    author = models.ForeignKey(Account, on_delete=models.CASCADE)
    content = models.TextField(null=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now_add=True)
