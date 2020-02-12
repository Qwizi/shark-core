from django.test import TestCase

from ..models import Account


class AccountModelsTestCase(TestCase):

    def setUp(self):
        # Test na koncie Qwizi -> https://steamcommunity.com/id/34534645645
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

    def test_create_user_steam_valid_steamid64(self):
        account = Account.objects.create_user_steam(steamid64=self.steamid64)

        self.assertEqual(account.steamid64, self.steamid64)
        self.assertEqual(account.steamid32, self.steamid32)
        self.assertEqual(account.steamid3, self.steamid3)
        self.assertEqual(account.username, self.username)
        self.assertEqual(account.avatar, self.avatar)
        self.assertEqual(account.avatarmedium, self.avatarmedium)
        self.assertEqual(account.avatarfull, self.avatarfull)
        self.assertEqual(account.loccountrycode, self.loccountrycode)
        self.assertEqual(account.display_group.id, self.user_group_id)
        self.assertEqual(account.display_group.name, self.user_group_name)
        self.assertEqual(account.groups.all().count(), 1)
        self.assertEqual(account.wallet_set.all().count(), 2)
        self.assertTrue(account.is_active)
        self.assertFalse(account.is_staff)
        self.assertFalse(account.is_superuser)

    def test_create_user_steam_invalid_steamid64(self):
        # Test na nie istniejacym koncie
        steamid64 = "3112121"

        with self.assertRaises(Exception) as context:
            Account.objects.create_user_steam(steamid64=steamid64)
        self.assertTrue("Invalid steamid64" in str(context.exception))

    def test_create_user_none_steamid64(self):
        steamid64 = None
        with self.assertRaises(Exception) as context:
            Account.objects.create_user_steam(steamid64=steamid64)
        self.assertTrue("Steamid64 cannot be None" in str(context.exception))

    def test_create_superuser_steam_valid_steamid64(self):
        account = Account.objects.create_superuser_steam(steamid64=self.steamid64)

        self.assertEqual(account.steamid64, self.steamid64)
        self.assertTrue(account.is_staff)
        self.assertTrue(account.is_active)
        self.assertTrue(account.is_superuser)

    def test_create_superuser_steam_invalid_steamid64(self):
        # Test na nie istniejacym koncie
        steamid64 = "3112121"

        with self.assertRaises(Exception) as context:
            Account.objects.create_superuser_steam(steamid64=steamid64)
        self.assertTrue("Invalid steamid64" in str(context.exception))

    def test_create_superuser_steam_none_steamid64(self):
        steamid64 = None

        with self.assertRaises(Exception) as context:
            Account.objects.create_superuser_steam(steamid64=steamid64)
        self.assertTrue("Steamid64 cannot be None" in str(context.exception))

    def test_account_activate(self):
        account = Account.objects.create_user_steam(steamid64=self.steamid64, is_active=False)

        self.assertFalse(account.is_active)

        account.activate()

        self.assertTrue(account.is_active)