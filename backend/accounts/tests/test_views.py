from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework_simplejwt.tokens import RefreshToken

from ..models import Account

from forum.models import (
    Category,
    Thread,
    Post
)


class AccountViewTestCase(TestCase):
    def setUp(self):
        self.steamid64 = "76561198190469450"
        self.steamid32 = "STEAM_1:0:115101861"
        self.steamid3 = "[U:1:230203722]"
        self.username = "Qwizi"
        self.user_group_id = 3

        self.client = APIClient()

    """
    Pomocnicze metody
    """

    def _login_user(self, steamid64: str = None):
        """
        Metoda ktora rejestruje/loguje uzytkownika
        """

        # Przypisujemy domyslna wartosc
        s_steamid64 = self.steamid64

        # Jezeli argument steamid64 jest uzupelniony przypisujemy odpowiedna wartosc
        if steamid64:
            s_steamid64 = steamid64

        # Rejestrujemy uzytkownika uzytkownika, lub logujemy jezeli istnieje juz w bazie
        self.client.login(steamid64=s_steamid64)

    def _get_token(self, user: Account = None) -> RefreshToken:
        """
        Metoda zwracajaca token dla danego uzytkownika
        """

        # Rejestrujemy domyslnego usera
        self._login_user()

        # Pobieramy dane zarejestrowanego usera
        t_user = Account.objects.get(steamid64=self.steamid64)

        # Jezeli argument user jest uzupelniony przypisujemy odpowiedna wartosc
        if user:
            t_user = user

        # Pobieramy token dla usera
        token = RefreshToken.for_user(t_user)

        return token

    def _create_credentials(self, token: RefreshToken = None):
        """
        Metoda ustawiajaca odpowiedni header dla autoryzacji
        """

        # Pobieramy token dla domyslnego usera
        c_token = self._get_token()

        # Jezli argument token jest uzupelniony przypisujemy odpowiedna wartosc
        if token:
            c_token = token

        # Ustawiamy odpowiedni header
        self.client.credentials(HTTP_AUTHORIZATION="Bearer {}".format(c_token.access_token))

    """
    Testy
    """

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
