from rest_framework.test import (
    APIRequestFactory,
    force_authenticate
)
from rest_framework_simplejwt.tokens import RefreshToken

from forum.models import (
    Category,
    Thread,
    Post
)

from ..models import Account
from ..views import (
    AccountListView,
    AccountMeView
)
from .mixins import AccountTestMixin


class AccountViewTestCase(AccountTestMixin):

    def setUp(self):
        super().setUp()
        self.account = Account.objects.create_user_steam(steamid64=self.steamid64)
        self.token = RefreshToken.for_user(self.account)

    def test_account_list_view(self):
        """
        Test sprawdzajacy poprawnosc implementacji widoku dla listy uzytkowników
        """

        # Pobranie widoku dla listy uzytkownikow
        account_list_view = AccountListView.as_view()

        request = self.factory.get('/api/accounts/')
        response = account_list_view(request)

        self.assertEqual(response.status_code, 200)

    def test_account_me_with_authenticate_view(self):
        """
        Test sprawdzajacy poprawnosc implementacji widoku dla danych zalogowanego uzytkownika
        """

        # Pobranie widoku dla danych zalogowanego uzytkownika
        view = AccountMeView.as_view()

        request = self.factory.get('/api/accounts/me/')

        # Zmuszamy uzytkownika do autoryzacji
        force_authenticate(request, user=self.account, token=self.token)

        response = view(request)
        self.assertEqual(response.status_code, 200)

    def test_account_me_without_authenticate_view(self):
        """
        Test sprawdzajacy poprawnosc implementacji widoku dla danych nie zalogowanego uzytkownika
        """

        # Pobranie widoku dla danych nie zalogowanego uzytkownika
        view = AccountMeView.as_view()
        request = self.factory.get('/api/accounts/me/')
        response = view(request)

        self.assertEqual(response.status_code, 401)


class AccountViewApiTestCase(AccountTestMixin):
    def test_account_register(self):
        """
        Test sprawdzajacy poprawnosc rejestracji uzykownika
        """

        # Rejestracja domyslnego uzykownika
        self._login_user()

        # Pobieranie tego uzytkownika
        account = Account.objects.get(steamid64=self.steamid64)

        self.assertEqual(account.steamid64, self.steamid64)
        self.assertEqual(account.display_group.id, self.user_group_id)

    def test_account_login(self):
        """
        Test sprawdzajacy poprawnosc logowania uzytkownika
        """

        # Rejestracja uzytkownika
        self._login_user()

        # Pobieranie zarejestrowanego uzytkownika

        account = Account.objects.get(steamid64=self.steamid64)

        # Logowanie uzytkownika
        self._login_user(account.steamid64)

        self.assertEqual(account.steamid64, self.steamid64)
        self.assertEqual(account.steamid32, self.steamid32)

    def test_account_login_invalid_steamid64(self):
        """
        Test sprawdzajacy pooprawnosc wyswietlania wyjatku, jezeli podano bledny steamid64
        """

        # Bledny steamid64
        steamid64 = "33234234"

        with self.assertRaises(Exception) as context:
            # Logowanie uzykownika
            self._login_user(steamid64)
        self.assertTrue("Invalid steamid64" in str(context.exception))

    def test_account_login_exists_username(self):
        """
        Test sprawdzajacy poprawnosc logowania drugiego konta z takim samym nickiem
        """

        # Steamid64 uzytkownika z podonmy istniejacym juz nickiem
        # https://steamcommunity.com/profiles/76561198188480002
        steamid64_qwizi = "76561198188480002"

        # Logujemy pierwszego domyslnego uzytkownika o nicku Qwizi
        self._login_user()

        # Logowanie drugiego uzytkownika o nicku qwizi
        self._login_user(steamid64=steamid64_qwizi)

        # Pobranie pierwszego uzytkownika
        first_account = Account.objects.get(steamid64=self.steamid64)
        # Pobranie drugiego uzytkownika
        second_account = Account.objects.get(steamid64=steamid64_qwizi)

        self.assertEqual(first_account.username, self.username)
        self.assertNotEqual(second_account.username, first_account.username)

    def test_account_list(self):
        """
        Test sprawdzający poprawność wyswietlania listy kont
        """
        # Steamid64 pierwszego uzytkownika
        steamid64_one = self.steamid64
        # Steamid64 drugiego uzytkownika
        steamid64_two = "76561198145076068"

        # Rejestrujemy pierwszego usera
        self._login_user(steamid64=steamid64_one)
        # Rejestrujemy drugiego usera
        self._login_user(steamid64=steamid64_two)

        response = self.client.get('/api/accounts/')

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['count'], 2)
        # Sprawdzamy czy steamid64 jest rowny pierwszemu uzytkownikowi
        self.assertEqual(response.data['results'][0]['steamid64'], steamid64_one)
        # Sprawdzamy czy steamid64 jest rowny drugiemu uzytkownikowi
        self.assertEqual(response.data['results'][1]['steamid64'], steamid64_two)

    def test_empty_account_list(self):
        """
        Test sprawdzajacy poprawnosc wyswietlania pustej listy kont
        """
        response = self.client.get('/api/accounts/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['count'], 0)
        self.assertEqual(response.data['results'], [])

    def test_account_me_with_authenticate(self):
        """
        Test sprawdzajacy poprawnosc wyswietlania danych zalogowanego uzytkownika
        """

        # Rejestrujemy domyslnego uzytkownika
        self._login_user()

        # Pobieramy uzytkonwika
        account = Account.objects.get(steamid64=self.steamid64)

        # Pobieramy token dla uzykownika
        token = self._get_token(account)

        # Ustawawiamy headery dla autoryzacji
        self._create_credentials(token)

        response = self.client.get('/api/accounts/me/')

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['steamid64'], self.steamid64)
        self.assertEqual(response.data['steamid32'], self.steamid32)
        self.assertEqual(response.data['steamid3'], self.steamid3)
        self.assertEqual(response.data['username'], self.username)
        self.assertEqual(response.data['display_group'], self.user_group_id)
        self.assertEqual(response.data['threads'], 0)
        self.assertEqual(response.data['posts'], 0)

    def test_account_me_count_threads_with_authenticate(self):
        """
        Test sprawdzający poprawnosc wyswietlania licznika tematow dla zalogowanego uzytkownika
        """

        # Rejestrujemy domyslnego uzytkownika
        self._login_user()

        # Pobieramy uzytkownika
        account = Account.objects.get(steamid64=self.steamid64)

        # Pobieramy token dla uzykownika
        token = self._get_token(account)

        # Ustawiamy headery
        self._create_credentials(token)

        # Tworzymy testową kategorie
        category = Category.objects.create(name="Testowa kategoria")
        # Tworzymy testowy temat, gdzie autorem jest stworzony uzytkownik
        Thread.objects.create(
            title="Testowy watek",
            content="Testowa tresc",
            author=account,
            category=category
        )

        response = self.client.get('/api/accounts/me/')

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['threads'], 1)
        self.assertEqual(response.data['posts'], 0)

    def test_account_me_count_posts_with_authenticate(self):
        """
        Test sprawdzajacy poprawnosc wyswietlania licznika postow uzytkownika
        """

        # Rejestrujemy domyslnego uzytkownika
        self._login_user()

        # Pobieramy uzytkownika
        account = Account.objects.get(steamid64=self.steamid64)

        # Pobieramy token dla uzykownika
        token = self._get_token(account)

        # Ustawiamy headery
        self._create_credentials(token)

        # Tworzymy testową kategorie
        category = Category.objects.create(name="Testowa kategoria")
        # Tworzymy testowy temat, gdzie autorem jest stworzony uzytkownik
        thread = Thread.objects.create(
            title="Testowy watek",
            content="Testowa tresc",
            author=account,
            category=category
        )
        # Tworzymy dwa testowe posty w utworzonym temacie
        Post.objects.bulk_create([
            Post(thread=thread, content="Testowa tresc", author=account),
            Post(thread=thread, content="Testowa tresc", author=account)
        ])

        response = self.client.get('/api/accounts/me/')

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['threads'], 1)
        self.assertEqual(response.data['posts'], 2)

    def test_account_me_without_authenticate(self):
        """
        Test sprawdzajacy poprawnosc wyswietlania danych dla nie zalogowanego uzytkownika
        """
        response = self.client.get('/api/accounts/me/')
        self.assertEqual(response.status_code, 401)
