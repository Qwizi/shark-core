from ..models import (
    Category,
    Thread,
    Post
)
from accounts.models import Account

from .mixins import ForumTestMixin


class ForumModelsTestCase(ForumTestMixin):

    def setUp(self):
        super().setUp()
        self.author = Account.objects.create_user_steam(steamid64=self.steamid64)

    def test_create_category(self):
        """
        Test sprawdzajacy poprawosc tworzenia kategorii
        """
        # Tworzenie domyslnej kategorii
        self._create_category()

        # Pobranie domyslnej kategoi
        category = Category.objects.get(name=self.category_name)
        # Pobranie liczny stworzonych kategorii
        categories_count = Category.objects.all().count()
        self.assertEqual(category.name, self.category_name)
        self.assertEqual(categories_count, 1)

    def test_create_thread(self):
        """
        Test sprawdzajacy poprawnosc tworzenia tematu
        """

        # Tworzenie domyslnego tematu
        self._create_thread()

        # Pobranie domyslnego tematu
        thread = Thread.objects.get(title=self.thread_title)
        # Pobranie liczby stworzonych tematow
        threads_count = Thread.objects.all().count()

        self.assertEqual(thread.title, self.thread_title)
        self.assertEqual(thread.content, self.thread_content)
        self.assertEqual(thread.category.name, self.category_name)
        self.assertEqual(thread.author.steamid64, self.author.steamid64)
        self.assertEqual(thread.last_poster, None)
        self.assertEqual(thread.status, Thread.ThreadStatusChoices.OPENED)
        self.assertEqual(threads_count, 1)
        self.assertFalse(thread.pinned)

    def test_create_post(self):
        """
        Test sprawdzajacy poprawnosc tworzenia posta
        """

        # Tworzenie domyslnego postu
        self._create_post()

        # Pobranie domyslnego postu
        post = Post.objects.get(content=self.post_content)
        # Licznik stworzonych postow
        posts_count = Post.objects.all().count()

        self.assertEqual(post.thread.title, self.thread_title)
        self.assertEqual(post.content, self.post_content)
        self.assertEqual(post.author.steamid64, self.author.steamid64)
        self.assertEqual(post.status, Post.PostStatusChoices.VISIBLE)
        self.assertEqual(posts_count, 1)

    def test_pin_thread(self):
        """
        Test sprawdzajacy poprawnosc przypinania tematu
        """

        # Tworzenie domyslnego tematu
        thread = self._create_thread()

        # Sprawdzenie czy temat napewno nie jest przypiety
        self.assertFalse(thread.pinned)

        # Przypiecie tematu
        thread.pin()

        # Pobranie tematu w celu sprawdzenia czy napewnop zostal przypiety
        pinned_thread = Thread.objects.get(title=self.thread_title)

        self.assertTrue(pinned_thread.pinned)

    def test_unpin_thread(self):
        """
        Test sprawdzajacy poprawnosc odpinania tematu
        """

        # Tworzenie domyslnego przypietego tematu
        thread = self._create_thread(pinned=True)

        # Sprawdzenie czy temat jest przypiety
        self.assertTrue(thread.pinned)

        # Odpiecie tematu
        thread.unpin()

        # Pobranie teamtu w celu sprawdzenia czy zostal odpiety
        unpinned_thread = Thread.objects.get(title=self.thread_title)

        self.assertFalse(unpinned_thread.pinned)

    def test_thread_status_choices(self):
        """
        Test sprawdzajacy poprawnosc ustawionych statusow tematow
        """
        CLOSED = 0
        OPENED = 1
        HIDDEN = -1

        self.assertEqual(Thread.ThreadStatusChoices.OPENED, OPENED)
        self.assertEqual(Thread.ThreadStatusChoices.CLOSED, CLOSED)
        self.assertEqual(Thread.ThreadStatusChoices.HIDDEN, HIDDEN)

    def test_open_thread(self):
        """
        Test sprawdzajacy poprawnosc otwierania tematu
        """

        # Tworzenie domyslnego zamknietego tematu
        thread = self._create_thread(status=Thread.ThreadStatusChoices.CLOSED)

        # Otwarcie tematu
        thread.open()

        # Sprawdzanie czy napewno temat zostal otwary
        opened_thread = Thread.objects.get(title=self.thread_title)

        self.assertEqual(opened_thread.status, Thread.ThreadStatusChoices.OPENED)

    def test_close_thread(self):
        """
        Test sprawdzajacy poprawnosc zamykania tematu
        """

        # Tworzenie domyslnego otwartego tematu
        thread = self._create_thread(status=Thread.ThreadStatusChoices.OPENED)

        # Zamkniecie tematu
        thread.close()

        # Sprawdzanie czy temat na pewno zostal zamkniety
        close_thread = Thread.objects.get(title=self.thread_title)

        self.assertEqual(close_thread.status, Thread.ThreadStatusChoices.CLOSED)

    def test_hide_thread(self):
        """
        Test sprawdzajacy poprawnoc ukrywania tematu
        """
        # Tworzenie domyslnego tematu
        thread = self._create_thread()

        # Ukrycie tematu
        thread.hide()

        # Sprawdzanie czy temat zostal napewno ukryty

        hidden_thread = Thread.objects.get(title=self.thread_title)
        self.assertEqual(hidden_thread.status, Thread.ThreadStatusChoices.HIDDEN)

    def test_post_status_choices(self):
        """
        Test sprawdzajacy poprawnosc statusow posta
        """
        VISIBLE = 1
        HIDDEN = 0

        # Tworzenie domyslnego posta
        post = self._create_post()

        self.assertEqual(post.PostStatusChoices.VISIBLE, VISIBLE)
        self.assertEqual(post.PostStatusChoices.HIDDEN, HIDDEN)

    def test_visible_post(self):
        """
        Test sprawdzajacy poprawnosc pokazywania posta
        """

        # Tworzenie domyslnego ukrytego posta
        post = self._create_post(status=Post.PostStatusChoices.HIDDEN)

        # Pokazywanie posta
        post.visible()

        # Sprawdzanie czy na pewno post jest widoczny

        visible_post = Post.objects.get(content=self.post_content)

        self.assertEqual(visible_post.status, Post.PostStatusChoices.VISIBLE)

    def test_hide_post(self):
        """
        Test sprawdzajacy poprawnosc ukrytwania posta
        """

        # Tworzenie domyslnego postu
        post = self._create_post()

        # Ukrycie posta
        post.hide()

        # Sprawdzanie czy post zostal napepwno ukryty

        hidden_post = Post.objects.get(content=self.post_content)

        self.assertEqual(hidden_post.status, Post.PostStatusChoices.HIDDEN)
