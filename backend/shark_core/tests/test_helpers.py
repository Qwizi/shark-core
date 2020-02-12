from django.test import TestCase

from ..helpers import (
    get_shark_core_settings,
    get_steam_setting,
    check_banned_usernames,
    create_random_username
)

from accounts.models import Account


class SharkCoreHelpersTestCase(TestCase):
    def test_get_shark_core_settings_valid_setting(self):
        setting = get_shark_core_settings("STEAM")
        self.assertTrue(setting)

    def test_get_shark_core_settings_invalid_setting(self):
        with self.assertRaises(Exception) as context:
            get_shark_core_settings("INVALID")
        self.assertTrue('Setting {} not exist in SHARK_CORE', format("INVALID") in str(context.exception))

    def test_get_steam_setting_valid_setting(self):
        setting = get_steam_setting('API_KEY')
        self.assertTrue(setting)

    def test_get_steam_setting_invalid_setting(self):
        with self.assertRaises(Exception) as context:
            get_steam_setting('INVALID')
        self.assertTrue('Setting {} not exist in STEAM'.format('INVALID') in str(context.exception))

    def test_check_banned_usernames_exist_username(self):
        banned_usernames = (
            r'^((a|A)dmin)$',
            r'^((a|a)dministrator)$',
        )
        username = check_banned_usernames("Admin", source=banned_usernames)
        account = Account.objects.create_user_steam(steamid64="76561198190469450", username=username)
        self.assertNotEqual(account.username, "Admin")

    def test_check_banned_usernames_not_exist_username(self):
        banned_usernames = (
            r'^((a|A)dmin)$',
            r'^((a|a)dministrator)$',
        )
        username = check_banned_usernames("Test", source=banned_usernames)
        account = Account.objects.create_user_steam(steamid64="76561198190469450", username=username)
        self.assertEqual(account.username, "Test")
