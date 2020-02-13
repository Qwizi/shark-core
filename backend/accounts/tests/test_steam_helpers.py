from ..steam_helpers import get_steam_user_info

from .mixins import AccountTestMixin


class AccountSteamHelperTestCase(AccountTestMixin):
    def test_get_steam_user_info_valid_steamid64(self):
        """
        Test sprawdzajacy poprawnosc zwracanych steamowych danych uzytkonika,
        gdy podano poprawne steamid64
        """

        # Pobieramy dane
        user_data = get_steam_user_info(steamid64=self.steamid64)

        self.assertEqual(user_data['steamid64'], self.steamid64)
        self.assertEqual(user_data['steamid32'], self.steamid32)
        self.assertEqual(user_data['steamid3'], self.steamid3)
        self.assertEqual(user_data['username'], self.username)
        self.assertEqual(user_data['avatar'], self.avatar)
        self.assertEqual(user_data['avatarmedium'], self.avatarmedium)
        self.assertEqual(user_data['avatarfull'], self.avatarfull)
        self.assertEqual(user_data['loccountrycode'], self.loccountrycode)

    def test_get_steam_user_info_invalid_steamid64(self):
        """
        Test sprawdzajacy poprawnosc wyswietlania wyjatku w przypadku jak
        podano bledny steamid64
        """
        steamid64 = "2412312123"

        with self.assertRaises(Exception) as context:
            get_steam_user_info(steamid64=steamid64)
        self.assertTrue("Invalid steamid64" in str(context.exception))
