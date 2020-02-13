from django.test import TestCase

from ..helpers import (
    get_shark_core_settings,
    get_steam_setting,
    check_banned_usernames,
)

from accounts.models import Account


class SharkCoreHelpersTestCase(TestCase):
    def test_get_shark_core_settings_valid_setting(self):
        """
        Test sprawdzajacy poprawnosc zwracanych ustawien SHARK_CORE
        gdy podano poprawna nazwe ustawien
        """
        setting = get_shark_core_settings("STEAM")
        self.assertTrue(setting)

    def test_get_shark_core_settings_invalid_setting(self):
        """
        Test sprawdzajacy poprawnosc wyswietlania wyjatku
        gdy podano bledna nazwe ustawien
        """

        invalid_setting = "INVALID"

        with self.assertRaises(Exception) as context:
            get_shark_core_settings(invalid_setting)
        self.assertTrue('Setting {} not exist in SHARK_CORE', format(invalid_setting) in str(context.exception))

    def test_get_steam_setting_valid_setting(self):
        """
        Test sprawdzajacy poprawnosc zwracanych ustawien STEAM
        gdy podano poprawna nazwe ustawien
        """
        setting = get_steam_setting('API_KEY')
        self.assertTrue(setting)

    def test_get_steam_setting_invalid_setting(self):
        """
        Test sprawdzajacy poprawnosc wyswietlania wyjatku
        gdy podano nie poprawna nazwe ustawien
        """

        invalid_setting = "INVALID"

        with self.assertRaises(Exception) as context:
            get_steam_setting(invalid_setting)
        self.assertTrue('Setting {} not exist in STEAM'.format(invalid_setting) in str(context.exception))

    def test_check_banned_usernames_exist_username(self):
        """
        Test sprawdzajacy, funkcje ktora sprawdza czy nazwa uzytkownika znajduje sie w liscie
        zbanowanych nazw uzytkownika
        """

        # Lista zbanowanych nazw uzytkownika
        banned_usernames = (
            r'^((a|A)dmin)$',
            r'^((a|a)dministrator)$',
        )

        # Nazwa uzytkownika, która powinna zostać znaleziona w liscie zbanowanych nazw
        username = check_banned_usernames("Admin", source=banned_usernames)
        # Tworzenie konta z inną losowa nazwą uzytkownika
        account = Account.objects.create_user_steam(steamid64="76561198190469450", username=username)
        self.assertNotEqual(account.username, "Admin")

    def test_check_banned_usernames_not_exist_username(self):
        """
        Test sprawdzajacy czy nazwa uzytkownika zostanie przepuszczona
        """
        banned_usernames = (
            r'^((a|A)dmin)$',
            r'^((a|a)dministrator)$',
        )
        # Nazwa uzytkownika, która powinna zostac przepuszczona
        username = check_banned_usernames("Test", source=banned_usernames)
        # Tworzenia konta z tą nazwą uzytkownika
        account = Account.objects.create_user_steam(steamid64="76561198190469450", username=username)
        self.assertEqual(account.username, "Test")
