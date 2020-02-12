from django.test import TestCase
from django.conf import settings

from ..steam_helpers import get_steam_user_info
from shark_core.helpers import get_steam_setting


class AccountSteamHelperTestCase(TestCase):

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

    def test_get_steam_user_info_valid_steamid64(self):
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
        steamid64 = "2412312123"

        with self.assertRaises(Exception) as context:
            user_data = get_steam_user_info(steamid64=steamid64)

        self.assertTrue("Invalid steamid64" in str(context.exception))
