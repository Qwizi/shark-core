from .mixins import ForumTestMixin

from rest_framework.test import force_authenticate
from rest_framework_simplejwt.tokens import RefreshToken

from ..views import (
    CategoryListView,
    CategoryDetailView,
    ThreadListView,
    ThreadCreateView,
    ThreadDetailView,
    PostListView,
    PostCreateView,
    PostDetailView
)

from ..models import (
    Category,
    Thread,
    Post
)

from accounts.models import Account


class ForumViewsTestCase(ForumTestMixin):

    def setUp(self):
        super().setUp()
        self.author = Account.objects.create_user_steam(steamid64=self.steamid64)

    def test_category_list_view(self):
        """
        Test sprawdzajacy poprawnosc implenetacji widoku listy kategorii
        """

        # Widok listy kategorii
        view = CategoryListView.as_view()
        request = self.factory.get('/api/forum/categories/')
        response = view(request)

        self.assertEqual(response.status_code, 200)

    def test_category_detail_view(self):
        """
        Test sprawdzajacy poprawnosc impletancji widoku detalu danej kategorii
        """

        # Tworzenie przykladowej kategorii
        category = Category.objects.create(name="Testowa kategoria")

        view = CategoryDetailView.as_view()
        request = self.factory.get('/api/forum/categories/')
        response = view(request, pk=category.pk)

        self.assertEqual(response.status_code, 200)

    def test_not_exist_category_detail_view(self):
        """
        Test sprawdzajacy poprawnosc implementacji widoku detalu dla nie istniejacej kategorii
        """

        view = CategoryDetailView.as_view()
        request = self.factory.get('/api/forum/categories/')
        response = view(request, pk=1)

        self.assertEqual(response.status_code, 404)

    def test_thread_list_view(self):
        """
        Test sprawdzajacy poprawnosc implenetacji widoku dla listy tematow
        """

        view = ThreadListView.as_view()
        request = self.factory.get('/api/forum/threads/')
        response = view(request)

        self.assertEqual(response.status_code, 200)

    def test_thread_detail_view(self):
        """
        Test sprawdzajacy poprawnosc implenetacji widoku detalu dla tematu
        """

        # Tworzenie przykladowej katogorii
        category = Category.objects.create(name="Przykladowa kategoria")

        # Tworzenie przykladowego autora
        # author = Account.objects.create(steamid64=self.steamid64)

        thread = Thread.objects.create(
            title="Przykladowy temat",
            content="Przykladowa tresc",
            author=self.author,
            category=category
        )

        view = ThreadDetailView.as_view()
        request = self.factory.get('/api/forum/threads/')
        response = view(request, pk=thread.pk)

        self.assertEqual(response.status_code, 200)

    def test_not_exists_thread_detail_view(self):
        """
        Test sprawdzajacy poprawnosc implementacji widoku detali dla nie istniejacego tematu
        """

        view = ThreadDetailView.as_view()
        request = self.factory.get('/api/forum/threads/')
        response = view(request, pk=99)

        self.assertEqual(response.status_code, 404)

    def test_thread_create_view(self):
        """
        Test sprawdzajacy poprawnosc implenetacji widoku tworzenia tematu
        """
        # Tworzenie domyslnej kategorii
        category = self._create_category()

        # Dane nowego postu
        new_thread_data = {
            'title': self.thread_title,
            'content': self.thread_content,
            'category': category.id
        }

        view = ThreadCreateView.as_view()
        request = self.factory.post('/api/forum/threads/create', data=new_thread_data)

        # Pobieramy token dla autora
        token = RefreshToken.for_user(self.author)

        # Wymuszamy autoryzacje
        force_authenticate(request, user=self.author, token=token.access_token)

        response = view(request)

        self.assertEqual(response.status_code, 201)

    def test_post_list_view(self):
        """
        Test sprawdzajacy poprawna implenetacje widoku listy postow
        """

        view = PostListView.as_view()
        request = self.factory.get('/api/forum/posts/')
        response = view(request)
        self.assertEqual(response.status_code, 200)

    def test_post_detail_view(self):
        """
        Test sprawdzajacy poprawna implementacje widoku pojedynczego postu
        """

        # Tworzenie domyslnego postu
        post = self._create_post()

        view = PostDetailView.as_view()
        request = self.factory.get('/api/forum/posts/')
        response = view(request, pk=post.pk)

        self.assertEqual(response.status_code, 200)

    def test_not_exist_post_detail_view(self):
        """
        Test sprawdzajacy poprawnosc implenetacji widoku nie istniejacego postu
        """

        view = PostDetailView.as_view()
        request = self.factory.get('/api/forum/posts/')
        response = view(request, pk=123)

        self.assertEqual(response.status_code, 404)

    def test_post_create_view(self):
        """
        Test sprawdzajacy poprawnosc implenetacji widoku tworzenia postu
        """

        # Tworzymy przykladowy temat
        thread = self._create_thread()

        new_thread_data = {
            'content': self.post_content,
            'thread': thread.pk
        }

        view = PostCreateView.as_view()
        request = self.factory.post('/api/forum/posts/create', data=new_thread_data)

        # Pobieramy token dla autora
        token = RefreshToken.for_user(self.author)

        # Wymuszamy autoryzacje
        force_authenticate(request, user=self.author, token=token.access_token)

        response = view(request)

        self.assertEqual(response.status_code, 201)


class ForumViewsApiTestCase(ForumTestMixin):

    def setUp(self):
        super().setUp()
        self.author = Account.objects.create_user_steam(steamid64=self.steamid64)

    def test_category_list(self):
        """
        Test sprawdzajacy poprawnosc wyswietlania listy kategorii
        """

        # Tworzenie domyslnej kategorii
        self._create_category()
        # Tworzenie drugiej kategorii
        self._create_category(category_name="Test")

        response = self.client.get('/api/forum/categories/')

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['count'], 2)
        self.assertEqual(response.data['results'][0]['name'], self.category_name)
        self.assertEqual(response.data['results'][1]['name'], "Test")

    def test_empty_category_list(self):
        """
        Test sprawdzajacy pooprawnosc wyswietlania pustej listy kategorii
        """

        response = self.client.get('/api/forum/categories/')

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['count'], 0)

    def test_category_detail(self):
        """
        Test sprawdzajacy poprawnosc wyswietlania detali danej kategorii
        """

        # Tworzenie domyslnej kategorii
        category = self._create_category()

        response = self.client.get('/api/forum/categories/{}/'.format(category.pk))

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['name'], category.name)

    def test_thread_list(self):
        """
        Test sprawdzajacy poprawnosc wyswietlania listy watkow
        """
        second_thread_title = "Drugi testowy tytuł wątku"
        second_thread_content = "Drugi testowa tresc wątku"
        second_thread_category_name = "Druga kategoria"

        first_thread = self._create_thread()
        second_thread = self._create_thread(
            title=second_thread_title,
            content=second_thread_content,
            category_name=second_thread_category_name
        )

        response = self.client.get('/api/forum/threads/')

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['count'], 2)
        self.assertEqual(response.data['results'][0]['title'], first_thread.title)
        self.assertEqual(response.data['results'][0]['content'], first_thread.content)
        self.assertEqual(response.data['results'][0]['category']['name'], first_thread.category.name)
        self.assertEqual(response.data['results'][1]['title'], second_thread.title)
        self.assertEqual(response.data['results'][1]['content'], second_thread.content)
        self.assertEqual(response.data['results'][1]['category']['name'], second_thread.category.name)

    def test_empty_thread_list(self):
        """
        Test sprawdzajacy poprawnosc wyswietlania pustej listy tematow
        """
        response = self.client.get('/api/forum/threads/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['count'], 0)

    def test_thread_detail(self):
        """
        Test sprawdzajacy poprawnosc wyswietlania detali danego tematu
        """

        thread = self._create_thread()

        response = self.client.get('/api/forum/threads/{}/'.format(thread.pk))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['title'], thread.title)

    def test_thread_create(self):
        """
        Test sprawdzajacy poprawnosc tworzenia nowego tematu
        """

        # Tworzenie domyslnej kategorii
        category = self._create_category()

        # Dane nowego tematu
        new_thread_data = {
            'title': self.thread_title,
            'content': self.thread_content,
            'category': category.id
        }

        # Pobieramy token dla autora
        token = RefreshToken.for_user(self.author)

        # Ustawiwamy naglowek autoryzacyjny
        self.client.credentials(HTTP_AUTHORIZATION="Bearer {}".format(token.access_token))

        response = self.client.post('/api/forum/threads/create', data=new_thread_data)

        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.data['title'], new_thread_data['title'])
        self.assertEqual(response.data['content'], new_thread_data['content'])
        self.assertEqual(response.data['category'], new_thread_data['category'])

    def test_thread_create_without_authenticate(self):
        """
        Test sprawdzajacy poprawnosc wyswietlania towrzenia nowego tematu
        gdy autor nie jest zalogowany
        """

        # Tworzenie domyslnej kategorii
        category = self._create_category()

        # Dane nowego tematu
        new_thread_data = {
            'title': self.thread_title,
            'content': self.thread_content,
            'category': category.id
        }

        response = self.client.post('/api/forum/threads/create', data=new_thread_data)

        self.assertEqual(response.status_code, 401)

    def test_thread_create_without_data(self):
        """
        Test sprawdzajacy poprawnosc wyswietlania tworzenia nowego tematu,
        gdy nie podano tytuly tematu
        """

        # Tworzenie domyslnej kategorii
        category = self._create_category()

        # Pobieramy token dla autora
        token = RefreshToken.for_user(self.author)

        # Ustawiwamy naglowek autoryzacyjny
        self.client.credentials(HTTP_AUTHORIZATION="Bearer {}".format(token.access_token))

        response = self.client.post('/api/forum/threads/create')

        self.assertEqual(response.status_code, 400)

    def test_post_list(self):
        """
        Test sprawdzajacy poprawnosc wyswietlania listy postow
        """

        # Tworzenie domyslnego postu
        self._create_post()

        response = self.client.get('/api/forum/posts/')

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['count'], 1)
        self.assertEqual(response.data['results'][0]['content'], self.post_content)

    def test_post_empty_list(self):
        """
        Test sprawdzajacy poprawnosc wyswietlania pustej listy postow
        """

        response = self.client.get('/api/forum/posts/')

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['count'], 0)

    def test_post_detail(self):
        """
        Test sprawdzajacy poprawnosc wyswietlania danych pojedynczego postu
        """

        # Tworzenie domyslnego postu
        post = self._create_post()

        response = self.client.get('/api/forum/posts/{}/'.format(post.id))

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['thread'], post.thread.id)
        self.assertEqual(response.data['content'], post.content)
        self.assertEqual(response.data['author']['username'], post.author.username)

    def test_post_create(self):
        """
        Test sprawdzajacy poprawnosc tworzenia posta
        """
        # Tworzymy przykladowy temat
        thread = self._create_thread()

        new_post_data = {
            'content': self.post_content,
            'thread': thread.id
        }

        # Pobieramy token dla autora
        token = RefreshToken.for_user(self.author)

        # Ustawiwamy naglowek autoryzacyjny
        self.client.credentials(HTTP_AUTHORIZATION="Bearer {}".format(token.access_token))

        response = self.client.post('/api/forum/posts/create', data=new_post_data)

        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.data['content'], new_post_data['content'])
        self.assertEqual(response.data['thread'], thread.id)

    def test_post_create_without_authenticate(self):
        """
        Test sprawdzajacy poprawnosc tworzenia posta,
        gdy autor nie jest zalogowany
        """

        # Tworzymy przykladowy temat
        thread = self._create_thread()

        new_post_data = {
            'content': self.post_content,
            'thread': thread.id
        }

        response = self.client.post('/api/forum/posts/create', data=new_post_data)

        self.assertEqual(response.status_code, 401)

    def test_post_create_without_data(self):
        """
        Test sprawdzajacy poprawnosc tworzenia posta,
        gdy nie podano danych
        """

        # Pobieramy token dla autora
        token = RefreshToken.for_user(self.author)

        # Ustawiwamy naglowek autoryzacyjny
        self.client.credentials(HTTP_AUTHORIZATION="Bearer {}".format(token.access_token))

        response = self.client.post('/api/forum/posts/create')

        self.assertEqual(response.status_code, 400)
