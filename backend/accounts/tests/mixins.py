from django.test import TestCase

from rest_framework.test import (
    APIClient,
    APIRequestFactory
)
from rest_framework_simplejwt.tokens import RefreshToken

from ..models import Account


class AccountTestMixin(TestCase):

    def setUp(self):
        self.steamid64 = "76561198190469450"
        self.steamid32 = "STEAM_1:0:115101861"
        self.steamid3 = "[U:1:230203722]"
        self.username = "Qwizi"
        self.avatar = "https://steamcdn-a.akamaihd.net/steamcommunity/public/images/avatars/35/35f3a0e0d3f895f4ae608ccf68ae4e7b262a544d.jpg"
        self.avatarmedium = "https://steamcdn-a.akamaihd.net/steamcommunity/public/images/avatars/35/35f3a0e0d3f895f4ae608ccf68ae4e7b262a544d_medium.jpg"
        self.avatarfull = "https://steamcdn-a.akamaihd.net/steamcommunity/public/images/avatars/35/35f3a0e0d3f895f4ae608ccf68ae4e7b262a544d_full.jpg"
        self.loccountrycode = "PL"
        self.user_group_id = 3
        self.user_group_name = "Users"

        self.client = APIClient()
        self.factory = APIRequestFactory()

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
