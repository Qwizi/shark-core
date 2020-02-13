from django.test import TestCase

from ..models import (
    Category,
    Thread,
    Post
)
from accounts.models import Account


class ForumModelsTestCase(TestCase):

    def setUp(self):
        self.steamid64 = "76561198190469450"
        self.category_name = "Testowa kategoria"
        self.thread_title = "Testowy temat"
        self.thread_content = "Testowy content"
        self.post_content = "Testowy content w poście"
        self.account = Account.objects.create_user_steam(steamid64=self.steamid64)

    def _create_category(self, category_name=None):
        if category_name:
            category = Category.objects.create(name=category_name)
        else:
            category = Category.objects.create(name=self.category_name)
        return category

    def _create_thread(self, **kwargs):
        category = self._create_category()

        thread = Thread.objects.create(
            title=self.thread_title,
            content=self.thread_content,
            author=self.account,
            category=category
        )
        return thread

    def _create_post(self, **kwargs):
        thread = self._create_thread()
        post = Post.objects.create(
            thread=thread,
            author=self.account,
            content=self.post_content
        )
        return post

    def test_create_category(self):
        category = self._create_category(self.category_name)
        self.assertEqual(category.name, self.category_name)

    def test_create_thread(self):
        thread = self._create_thread()
        self.assertEqual(thread.title, self.thread_title)
        self.assertEqual(thread.content, self.thread_content)
        self.assertEqual(thread.category.name, self.category_name)
        self.assertEqual(thread.author.steamid64, self.account.steamid64)
        self.assertEqual(thread.last_poster, None)
        self.assertEqual(thread.status, 1)
        self.assertFalse(thread.pinned)

    def test_create_post(self):
        post = self._create_post()
        self.assertEqual(post.thread.title, self.thread_title)
        self.assertEqual(post.content, self.post_content)
        self.assertEqual(post.author.steamid64, self.account.steamid64)

    def test_pin_thread(self):
        thread = self._create_thread()
        thread.pin()
        self.assertTrue(thread.pinned)

    def test_unpin_thread(self):
        thread = self._create_thread()
        thread.unpin()
        self.assertFalse(thread.pinned)

    def test_thread_status_choices(self):
        CLOSED = 0
        OPENED = 1
        HIDDEN = -1

        thread = self._create_thread()

        self.assertEqual(thread.ThreadStatusChoices.OPENED, OPENED)
        self.assertEqual(thread.ThreadStatusChoices.CLOSED, CLOSED)
        self.assertEqual(thread.ThreadStatusChoices.HIDDEN, HIDDEN)

    def test_open_thread(self):
        thread = self._create_thread()
        thread.open()
        self.assertEqual(thread.status, thread.ThreadStatusChoices.OPENED)

    def test_close_thread(self):
        thread = self._create_thread()
        thread.close()
        self.assertEqual(thread.status, thread.ThreadStatusChoices.CLOSED)

    def test_hide_thread(self):
        thread = self._create_thread()
        thread.hide()
        self.assertEqual(thread.status, thread.ThreadStatusChoices.HIDDEN)

    def test_post_status_choices(self):
        VISIBLE = 1
        HIDDEN = 0

        post = self._create_post()

        self.assertEqual(post.PostStatusChoices.VISIBLE, VISIBLE)
        self.assertEqual(post.PostStatusChoices.HIDDEN, HIDDEN)

    def test_visible_post(self):
        post = self._create_post()
        post.visible()
        self.assertEqual(post.status, post.PostStatusChoices.VISIBLE)

    def test_hide_post(self):
        post = self._create_post()
        post.hide()
        self.assertEqual(post.status, post.PostStatusChoices.HIDDEN)
