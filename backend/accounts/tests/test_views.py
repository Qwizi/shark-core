from django.test import TestCase
from rest_framework.test import APIClient

from ..models import Account

from rest_framework_simplejwt.tokens import RefreshToken


class AccountViewTestCase(TestCase):

    def setUp(self):
        self.steamid64 = "76561198190469450"
        self.steamid32 = "STEAM_1:0:115101861"
        self.steamid3 = "[U:1:230203722]"
        self.username = "Qwizi"
        self.user_group_id = 3

        self.client = APIClient()

    def test_account_list(self):
        steamid64_one = self.steamid64
        steamid64_two = "76561198145076068"

        Account.objects.create_user_steam(steamid64=steamid64_one)
        Account.objects.create_user_steam(steamid64=steamid64_two)

        response = self.client.get('/api/accounts/')

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['count'], 2)
        self.assertEqual(response.data['results'][0]['steamid64'], steamid64_one)
        self.assertEqual(response.data['results'][1]['steamid64'], steamid64_two)

    def test_empty_account_list(self):
        response = self.client.get('/api/accounts/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['count'], 0)
        self.assertEqual(response.data['results'], [])

    def test_empty_account_list_without_endslash_redirect(self):
        response = self.client.get('/api/accounts')
        self.assertEqual(response.status_code, 301)

    def test_account_me_with_authenticate(self):
        account = Account.objects.create_user_steam(steamid64=self.steamid64)

        token = RefreshToken.for_user(account)

        self.client.credentials(HTTP_AUTHORIZATION="Bearer {}".format(token.access_token))

        response = self.client.get('/api/accounts/me/')

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['steamid64'], self.steamid64)
        self.assertEqual(response.data['steamid32'], self.steamid32)
        self.assertEqual(response.data['steamid3'], self.steamid3)
        self.assertEqual(response.data['username'], self.username)
        self.assertEqual(response.data['display_group'], self.user_group_id)

    def test_account_me_without_authenticate(self):
        response = self.client.get('/api/accounts/me/')
        self.assertEqual(response.status_code, 401)

    def test_account_register(self):
        self.client.login(steamid64=self.steamid64)
        self.assertEqual(Account.objects.get(steamid64=self.steamid64).steamid64, self.steamid64)
        self.assertEqual(Account.objects.get(steamid64=self.steamid64).display_group.id, self.user_group_id)
        # print(Account.objects.get(steamid64=self.steamid64))

    def test_account_login(self):
        Account.objects.create_user_steam(steamid64=self.steamid64)
        self.client.login(steamid64=Account.objects.get(steamid64=self.steamid64).steamid64)
        self.assertEqual(Account.objects.get(steamid64=self.steamid64).steamid64, self.steamid64)
        self.assertEqual(Account.objects.get(steamid64=self.steamid64).steamid32, self.steamid32)

    def test_account_login_invalid_steamid64(self):
        steamid64 = "33234234"

        with self.assertRaises(Exception) as context:
            self.client.login(steamid64=steamid64)
        self.assertTrue("Invalid steamid64" in str(context.exception))

    def test_account_login_exists_username(self):
        steamid64_qwizi = "76561198188480002"

        self.client.login(steamid64=self.steamid64)

        # Logowanie na konto o nicku qwizi https://steamcommunity.com/profiles/76561198188480002
        self.client.login(steamid64=steamid64_qwizi)

        print(Account.objects.get(steamid64="76561198188480002").username)
        self.assertEqual(Account.objects.get(steamid64=self.steamid64).username, self.username)
        self.assertNotEqual(Account.objects.get(steamid64=steamid64_qwizi).username, Account.objects.get(steamid64=self.steamid64).username, self.username)
