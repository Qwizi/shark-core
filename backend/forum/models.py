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
        HIDDEN = -1

    title = models.CharField(max_length=80)
    content = models.TextField()
    category = models.ForeignKey(Category, on_delete=models.CASCADE, null=True)
    author = models.ForeignKey(Account, on_delete=models.CASCADE, related_name='thread_author_set')
    last_poster = models.ForeignKey(Account, on_delete=models.CASCADE, related_name='last_poster', null=True)
    status = models.IntegerField(choices=ThreadStatusChoices.choices, default=ThreadStatusChoices.OPENED)
    pinned = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return '{} | {} | {}'.format(self.title, self.author.username, self.status)

    def pin(self):
        self.pinned = True
        self.save()

    def unpin(self):
        self.pinned = False
        self.save()

    def open(self):
        self.status = self.ThreadStatusChoices.OPENED
        self.save()

    def close(self):
        self.status = self.ThreadStatusChoices.CLOSED
        self.save()

    def hide(self):
        self.status = self.ThreadStatusChoices.HIDDEN
        self.save()


class Post(models.Model):

    class PostStatusChoices(models.IntegerChoices):
        VISIBLE = 1
        HIDDEN = 0

    thread = models.ForeignKey(Thread, on_delete=models.CASCADE)
    author = models.ForeignKey(Account, on_delete=models.CASCADE, related_name="post_author_set")
    content = models.TextField()
    status = models.IntegerField(choices=PostStatusChoices.choices, default=PostStatusChoices.VISIBLE)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return '{} | {} | {}'.format(self.pk, self.thread.title, self.author.username)

    def visible(self):
        self.status = self.PostStatusChoices.VISIBLE
        self.save()

    def hide(self):
        self.status = self.PostStatusChoices.HIDDEN
        self.save()

    def update_thread_last_poster(self):
        self.thread.last_poster = self.author
        self.thread.save()

    def save(self, *args, **kwargs):
        self.update_thread_last_poster()
        super(Post, self).save(*args, **kwargs)


class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    author = models.ForeignKey(Account, on_delete=models.CASCADE)
    content = models.TextField(null=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now_add=True)
