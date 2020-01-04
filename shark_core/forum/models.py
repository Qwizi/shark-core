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
    categories = models.ManyToManyField(Category)
    author = models.ForeignKey(Account, on_delete=models.CASCADE, related_name='author')
    last_poster = models.ForeignKey(Account, on_delete=models.CASCADE, related_name='last_poster')
    likes = models.IntegerField()
    status = models.IntegerField(choices=ThreadStatusChoices.choices, default=ThreadStatusChoices.OPENED)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return '{} | {} | {}'.format(self.title, self.author.username, self.status)


class Post(models.Model):
    thread = models.ForeignKey(Thread, on_delete=models.CASCADE)
    author = models.ForeignKey(Account, on_delete=models.CASCADE)
    content = models.TextField()
    likes = models.IntegerField()
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return '{} | {} | {}'.format(self.pk, self.thread.title, self.author.username)


class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    author = models.ForeignKey(Account, on_delete=models.CASCADE)
    content = models.TextField(null=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now_add=True)

