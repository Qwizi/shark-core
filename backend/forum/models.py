from django.db import models
from accounts.models import Account


class ReactionItem(models.Model):
    name = models.CharField(max_length=64, unique=True)
    tag = models.CharField(max_length=64, unique=True)
    image = models.URLField(default='http://localhost:3000/images/reactions/thx.png')


class Reaction(models.Model):
    item = models.ForeignKey(ReactionItem, on_delete=models.CASCADE)
    user = models.ForeignKey(Account, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.item.name} | {self.user.username}'


class SubCategory(models.Model):
    name = models.CharField(max_length=64, unique=True)

    def __str__(self):
        return f'{self.name}'


class Category(models.Model):
    name = models.CharField(max_length=64, unique=True)
    subcategories = models.ManyToManyField(SubCategory)

    def __str__(self):
        return f'{self.name}'


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
    reactions = models.ManyToManyField(Reaction)

    def __str__(self):
        return f'{self.title} | {self.author.username} | {self.status}'

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
    reactions = models.ManyToManyField(Reaction)
    best_answer = models.BooleanField(default=False)
    promotion_answer = models.BooleanField(default=False)

    def __str__(self):
        return f'{self.pk} | {self.thread.title} | {self.author.username}'

    def visible(self):
        self.status = self.PostStatusChoices.VISIBLE
        self.save()

    def hide(self):
        self.status = self.PostStatusChoices.HIDDEN
        self.save()

    def update_thread_last_poster(self):
        self.thread.last_poster = self.author
        self.thread.save()

    def set_best_answer(self):
        self.best_answer = True
        self.save()

    def unset_best_answer(self):
        self.best_answer = False
        self.save()

    def save(self, *args, **kwargs):
        self.update_thread_last_poster()
        super(Post, self).save(*args, **kwargs)
