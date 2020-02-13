from django.test import TestCase

from rest_framework.test import APIClient

from ..models import (
    Category,
    Thread,
    Post
)
from accounts.models import Account


class ForumViewsTestCase(TestCase):

    def setUp(self):
        self.steamid64 = "76561198190469450"
        self.category_name = "Testowa kategoria"
        self.thread_title = "Testowy temat"
        self.thread_content = "Testowy content"
        self.post_content = "Testowy content w poście"
        self.account = Account.objects.create_user_steam(steamid64=self.steamid64)
        self.client = APIClient()

    def _create_category(self, category_name=None):
        if category_name:
            category = Category.objects.create(name=category_name)
        else:
            category = Category.objects.create(name=self.category_name)
        return category

    def _create_thread(self, title=None, content=None, author=None, category=None):
        t_category = self._create_category(category)
        t_title = self.thread_title
        t_content = self.thread_content
        t_author = self.account

        if title:
            t_title = title

        if content:
            t_content = content

        if author:
            t_author = author

        thread = Thread.objects.create(
            title=t_title,
            content=t_content,
            author=t_author,
            category=t_category
        )
        return thread

    def test_categories_list(self):
        self._create_category()
        self._create_category(category_name="Test")

        response = self.client.get('/api/forum/categories/')

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['count'], 2)
        self.assertEqual(response.data['results'][0]['name'], self.category_name)
        self.assertEqual(response.data['results'][1]['name'], "Test")

    def test_empty_categories_list(self):
        response = self.client.get('/api/forum/categories/')

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['count'], 0)

    def test_empty_categories_list_redirect_without_endslash(self):
        response = self.client.get('/api/forum/categories')

        self.assertEqual(response.status_code, 301)

    def test_threads_list(self):
        second_thread_title = "Drugi testowy tytuł wątku"
        second_thread_content = "Drugi testowa tresc wątku"
        second_thread_category_name = "Druga kategoria"

        self._create_thread()
        self._create_thread(
            title=second_thread_title,
            content=second_thread_content,
            category=second_thread_category_name
        )

        primary_category = Category.objects.get(name=self.category_name)
        second_category = Category.objects.get(name=second_thread_category_name)

        response = self.client.get('/api/forum/threads/')

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['count'], 2)
        self.assertEqual(response.data['results'][0]['title'], self.thread_title)
        self.assertEqual(response.data['results'][0]['content'], self.thread_content)
        self.assertEqual(response.data['results'][0]['category']['name'], self.category_name)
        self.assertEqual(response.data['results'][1]['title'], second_thread_title)
        self.assertEqual(response.data['results'][1]['content'], second_thread_content)
        self.assertEqual(response.data['results'][1]['category']['name'], second_thread_category_name)

    def test_empty_threads_list(self):
        response = self.client.get('/api/forum/threads/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['count'], 0)

    def test_empty_threads_list_redirect_without_endslash(self):
        response = self.client.get('/api/forum/threads')
        self.assertEqual(response.status_code, 301)
