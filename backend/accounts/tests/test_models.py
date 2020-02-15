from ..models import (
    Account,
    Role,
    Wallet,
    BonusCode,
    SMSNumber,
    PaymentMethod
)

from djmoney.money import Money

from .mixins import AccountTestMixin

from ..providers import payment_manager


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

    def test_account_update_display_role(self):
        """
        Test sprawdzajacy poprawnosc aktualizwania wyswietlanej roli
        """

        # Tworzenie domyslnego uzytkownika
        account = Account.objects.create_user_steam(steamid64=self.steamid64)

        # Rola uzytkownika
        user_role = Role.objects.get(name="User")
        # Rola admina
        admin_role, created = Role.objects.get_or_create(name="Admin")

        self.assertEqual(account.display_role, user_role)

        # Dodanie roli Admin do rol uzytkownika
        account.roles.add(admin_role)

        account.update_display_role(admin_role)

        self.assertEqual(account.display_role, admin_role)

    def test_account_on_created_wallet_exist(self):
        """
        Test sprawdzajacy poprawnosc tworzenia portfeli w chwili utworzenia konta
        """

        # Tworzymy konto
        account = Account.objects.create_user_steam(steamid64=self.steamid64)

        self.assertEqual(account.wallet_set.all().count(), 2)
        self.assertEqual(account.wallet_set.all()[0].wtype, Wallet.WalletTypeChoices.PRIMARY)
        self.assertEqual(account.wallet_set.all()[1].wtype, Wallet.WalletTypeChoices.SECONDARY)

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

    def test_paymentmethod_create(self):
        # Tworzymy metode platnosci
        payment_method = PaymentMethod.objects.create(name=PaymentMethod.PaymentChoices.CODE)

        self.assertEqual(payment_method.name, PaymentMethod.PaymentChoices.CODE)

    def test_wallet_create(self):
        """
        Test sprawdzajacy poprawnosc tworzenia portfela
        """

        # Tworzymy domyslnego uzytkwonika
        account = Account.objects.create_user_steam(steamid64=self.steamid64)

        # Tworzymy porfel dla uzytkownika
        wallet = Wallet.objects.create(
            wtype=Wallet.WalletTypeChoices.OTHER,
            account=account
        )

        self.assertEqual(wallet.account, account)
        self.assertEqual(wallet.wtype, Wallet.WalletTypeChoices.OTHER)

    def test_wallet_add_money_integers(self):
        """
        Test sprawdzajacy poprawne dodawanie pieniedzy do portfela
        gdy podano liczbe zalkowitą
        """

        # Tworzymy domyslnego uztykownika
        account = Account.objects.create_user_steam(self.steamid64)

        # Pobieramy podstawowy porfel uzytkownika
        wallet = account.wallet_set.get(wtype=Wallet.WalletTypeChoices.PRIMARY)

        self.assertEqual(wallet.money, Money(0, 'PLN'))

        # Ustalamy jaka wartosc pieniedzy chcemy dodac, w tym przypdaku jest to 5 PLN
        money_to_add = Money(5, 'PLN')

        # Ustalamy jaka powinna byc wartosc pieniedzy po dodanu
        except_money = Money(10, 'PLN')

        # Dodajemy pieniadze
        wallet.add_money(money_to_add)
        wallet.add_money(money_to_add)

        self.assertEqual(wallet.money, except_money)

    def test_wallet_add_money_floats(self):
        """
        Test sprawdzajacy poprawnosc dodawania pienidedzy do portfela
        gdy podano liczbe zmiennoprzecinkową
        """

        # Tworzymy domyslnego uztykownika
        account = Account.objects.create_user_steam(self.steamid64)

        # Pobieramy podstawowy porfel uzytkownika
        wallet = account.wallet_set.get(wtype=Wallet.WalletTypeChoices.PRIMARY)

        self.assertEqual(wallet.money, Money(0, 'PLN'))

        # Ustalamy jaka wartosc pieniedzy chcemy dodac, w tym przypdaku jest to 5.50 PLN
        money_to_add = Money(5.50, 'PLN')

        # Ustalamy jaka powinna byc wartosc pieniedzy po dodanu
        except_money = Money(11, 'PLN')

        # Dodajemy pieniadze
        wallet.add_money(money_to_add)
        wallet.add_money(money_to_add)

        self.assertEqual(wallet.money, except_money)

    def test_wallet_subtract_money_integers(self):
        """
        Test sprawdzajacy poprawnosc odejmowania pieniedzy z portfela
        gdy podano liczbe calkowita
        """

        # Tworzymy domyslnego uztykownika
        account = Account.objects.create_user_steam(self.steamid64)

        # Pobieramy podstawowy porfel uzytkownika
        wallet = account.wallet_set.get(wtype=Wallet.WalletTypeChoices.PRIMARY)
        wallet.money = Money(10, 'PLN')
        wallet.save()

        self.assertEqual(wallet.money, Money(10, 'PLN'))

        # Ustalamy jaka wartosc pieniedzy chcemy odjac, w tym przypdaku jest to 5.50 PLN
        money_to_subtract = Money(5, 'PLN')

        # Ustalamy jaka powinna byc wartosc pieniedzy po dodanu
        except_money = Money(5, 'PLN')

        # Dodajemy pieniadze
        wallet.subtract_money(money_to_subtract)

        self.assertEqual(wallet.money, except_money)

    def test_bonus_code_create(self):
        # Testowy kod
        code = "TEST"

        # Tworzymy nowy kod bonusowy
        bonus_code = BonusCode.objects.create(
            code=code,
            money=Money(2, 'PLN')
        )

        self.assertEqual(bonus_code.code, code)
        self.assertEqual(bonus_code.money, Money(2, 'PLN'))

    def test_smsnumber_create(self):
        # Tworzymy przykladowy numer sms dla providera liveserver

        smsnumber = SMSNumber.objects.create(
            provider='liveserver',
            number=7222,
            expanse=Money(5, 'PLN'),
            money=Money(2.50, 'PLN')
        )

        self.assertEqual(smsnumber.provider, 'liveserver')
        self.assertEqual(smsnumber.number, 7222)
        self.assertEqual(smsnumber.expanse, Money(5, 'PLN'))
        self.assertEqual(smsnumber.money, Money(2.50, 'PLN'))

    def test_wallet_add_money_bonuscodes_payment_method(self):
        # Testowy kod
        code = "TEST"
        money = Money(5, 'PLN')

        # Tworzymy bonusowy kod
        bonus_code = BonusCode.objects.create(
            code=code,
            money=money
        )

        # Tworzymy konto uzykownika
        account = Account.objects.create_user_steam(steamid64=self.steamid64)

        # Pobieramy dodatkowy porfel uzytkownika
        secondary_wallet = account.wallet_set.get(wtype=Wallet.WalletTypeChoices.SECONDARY)

        self.assertEqual(secondary_wallet.money, Money(0, 'PLN'))

        # Pobieramy metode platnosci
        payment_bonus_code = PaymentMethod.objects.get(name=PaymentMethod.PaymentChoices.CODE)

        # Sprawdzamy czy portfel obsluguje platnosc kodem bonusowym
        # Jezeli tak pobieramy menadzer plantosci
        self.assertTrue(payment_bonus_code in secondary_wallet.payment_methods.all())

        if payment_bonus_code in secondary_wallet.payment_methods.all():
            # Pobieramy domyslny provider od platnosci kodem bonusowym
            provider_class = payment_manager.bonuscodes.get_provider_class()
            provider_instance = provider_class(model=BonusCode, code=bonus_code.code)

            # Walidujemy podany kod
            self.assertTrue(provider_instance.is_valid())

            # Jezeli jest zwalidowany pobieramy wartosc dodatkowych pieniedzy
            if provider_instance.is_valid():
                money_to_add = provider_instance.get_money()

                # Doladowywujemy portfel
                secondary_wallet.add_money(money_to_add)

                self.assertEqual(secondary_wallet.money, Money(5, 'PLN'))