from ..models import (
    Account,
    Role
)

from .mixins import AccountTestMixin


class AccountModelsTestCase(AccountTestMixin):

    def setUp(self):
        super().setUp()
        self.role_name = 'Testowa rola'
        self.role_format = '<span color="rgb(113,118,114)">{username}</span>'

    def test_account_create_user_steam_valid_steamid64(self):
        """
        Test sorawdzajacy poprawnosc tworzenia uzytkownika
        """
        # Tworzenie domyslnego uzytkownika
        account = Account.objects.create_user_steam(steamid64=self.steamid64)

        self.assertEqual(account.steamid64, self.steamid64)
        self.assertEqual(account.steamid32, self.steamid32)
        self.assertEqual(account.steamid3, self.steamid3)
        self.assertEqual(account.username, self.username)
        self.assertEqual(account.avatar, self.avatar)
        self.assertEqual(account.avatarmedium, self.avatarmedium)
        self.assertEqual(account.avatarfull, self.avatarfull)
        self.assertEqual(account.loccountrycode, self.loccountrycode)
        self.assertEqual(account.display_role.id, self.user_role_id)
        self.assertEqual(account.display_role.name, self.user_role_name)
        self.assertEqual(account.roles.all().count(), 1)
        self.assertEqual(account.wallet_set.all().count(), 2)
        self.assertTrue(account.is_active)
        self.assertFalse(account.is_staff)
        self.assertFalse(account.is_superuser)

    def test_account_create_user_steam_invalid_steamid64(self):
        """
        Test sprawdzajacy poprawnosc wyswietlania wyjatku w przypadku jak podano niepoprawny steamid64
        """
        # Niepoprawny steamid64
        steamid64 = "3112121"

        with self.assertRaises(Exception) as context:
            # Tworznie uzytkownika
            Account.objects.create_user_steam(steamid64=steamid64)
        self.assertTrue("Invalid steamid64" in str(context.exception))

    def test_account_create_user_none_steamid64(self):
        """
        Test sprawdzajacy poprawnosc wyswietlania wyjatku w przypadku gdy steamid64 jest rowne None
        """

        steamid64 = None
        with self.assertRaises(Exception) as context:
            # Tworzenie uzytkownika
            Account.objects.create_user_steam(steamid64=steamid64)
        self.assertTrue("Steamid64 cannot be None" in str(context.exception))

    def test_account_create_superuser_steam_valid_steamid64(self):
        """
        Test sprawdzajacy poprawnosc tworznie super uzytkownika
        """

        # Tworzenie super uzytkownika
        account = Account.objects.create_superuser_steam(steamid64=self.steamid64)

        self.assertEqual(account.steamid64, self.steamid64)
        self.assertTrue(account.is_staff)
        self.assertTrue(account.is_active)
        self.assertTrue(account.is_superuser)

    def test_account_create_superuser_steam_invalid_steamid64(self):
        """
        Test sprawdzajacy poprawnosc wyswietlania wyjatku w czasie tworzenia super uzytkownika
        gdy steamid 64 jest niepoprawne
        """

        # Niepoprawnie steamid64
        steamid64 = "3112121"

        with self.assertRaises(Exception) as context:
            Account.objects.create_superuser_steam(steamid64=steamid64)
        self.assertTrue("Invalid steamid64" in str(context.exception))

    def test_account_create_superuser_steam_none_steamid64(self):
        """
        Test sprawdzajacy poprawnosc wyswietlania wyjatku w czasie tworznia super uzytkownika
        gdy steamid64 jest rowne None
        """
        steamid64 = None

        with self.assertRaises(Exception) as context:
            Account.objects.create_superuser_steam(steamid64=steamid64)
        self.assertTrue("Steamid64 cannot be None" in str(context.exception))

    def test_account_activate(self):
        """
        Test sprawdzajacy poprawnosc aktywacji konta uzytkownika
        """
        # Tworzenie nie aktywnego konta uzytkownika
        account = Account.objects.create_user_steam(steamid64=self.steamid64, is_active=False)

        # Sprawdzamy czy konto jest na pewno nie aktywne
        self.assertFalse(account.is_active)

        # Aktywujemy konto
        account.activate()

        # Sprawdzamy czy konto zostalo aktywowne
        account_activated = Account.objects.get(pk=account.pk)

        self.assertTrue(account_activated.is_active)

    def test_role_create(self):
        """
        Test sprawdzajacy poprawnosc tworzenia roli
        """
        Role.objects.create(
            name=self.role_name,
            format=self.role_format
        )

        role = Role.objects.get(name=self.role_name)

        self.assertEqual(role.name, self.role_name)
        self.assertEqual(role.format, self.role_format)

    def test_role_create_random_color_format(self):
        """
        Test sprawdzajacy poprawnosc tworzenia losowego koloru w formacie roli
        """

        # Tworzymy role
        role = Role.objects.create(
            name=self.role_name
        )

        # Tworzymy format z losowym kolorem
        role.create_random_color_format()

        self.assertNotEqual(role.format, self.role_format)
