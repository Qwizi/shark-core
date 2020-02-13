from django.test import TestCase

from rest_framework.test import (
    APIClient,
    APIRequestFactory,
)

from accounts.models import Account

from ..models import (
    Category,
    Thread,
    Post
)


class ForumTestMixin(TestCase):
    def setUp(self):
        self.steamid64 = "76561198190469450"
        self.category_name = "Testowa kategoria"
        self.thread_title = "Testowy temat"
        self.thread_content = "Testowy content"
        self.post_content = "Testowy content w poście"
        self.client = APIClient()
        self.factory = APIRequestFactory()
        self.author = None

    def _create_category(self, category_name: str = None) -> Category:
        """
        Metoda tworzaca kategorie
        """

        # Przypisane domyslnej nazwy kategorii
        c_category_name = self.category_name

        # Jezli argument category_name jest uzupelniony przypiujemy odpowiedna wartosc
        if category_name:
            c_category_name = category_name

        # Tworzenie kategorii
        category = Category.objects.create(name=c_category_name)

        return category

    def _create_thread(self, category_name: str = None, title: str = None, content: str = None,
                       author: Account = None, **kwargs) -> Thread:
        """
        Metoda tworzaca temat
        """

        # Tworzenie kategorii
        category = self._create_category(category_name)

        # Przypisanie domyslnego tytuly dla tematu
        t_title = self.thread_title

        # Jezeli argument title jest ustawiony przypisujemy odpowiedna wartosc
        if title:
            t_title = title

        # Przypisanie domyslej tresci dla tematu
        t_content = self.thread_content

        # Jezeli argument content jest ustawiony przypisujemy odpowiedna wartosc
        if content:
            t_content = content

        # Przypisanie domyslnego autora dla tematu
        t_author = self.author

        # Jezeli argument author jest ustawiony przypisujemy odpowiedna wartosc
        if author:
            t_author = author

        # Tworzenie tematu
        thread = Thread.objects.create(
            title=t_title,
            content=t_content,
            author=t_author,
            category=category,
            **kwargs
        )
        return thread

    def _create_post(self, thread: Thread = None, author: Account = None, content: str = None, **kwargs) -> Post:
        """
        Metoda tworzaca post
        """

        # Jezeli argument thread jest ustawiony przypisujemy odpowiedna wartosc
        if thread:
            p_thread = thread
        else:
            p_thread = self._create_thread()

        # Przypisanie domyslnego autora dla tematu
        p_author = self.author

        # Jezeli argument author jest ustawiony przypisujemy odpowiedna wartosc
        if author:
            p_author = author

        # Przypisanie domyslnego tresci dla posta
        p_content = self.post_content

        # Jezeli argument content jest ustawiony przypisujemy odpowiedna wartosc
        if content:
            p_content = content

        # Tworzenie postu
        post = Post.objects.create(
            thread=p_thread,
            author=p_author,
            content=p_content,
            **kwargs
        )
        return post
