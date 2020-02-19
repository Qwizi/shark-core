import pytest

from django.urls import reverse

from .fixtures import *

from ..views import (
    RoleListView,
    RoleDetailView,
    AccountListView,
    AccountMeView,
    AccountMeUpdateDisplayRoleView,
    AccountMeWalletListView,
    AccountMeWalletExchangeView
)

"""
API REQUEST FACTORY
"""


@pytest.mark.django_db
def test_role_list_view(api_factory):
    view = RoleListView.as_view()
    request = api_factory.get(reverse('api:accounts:role-list'))
    response = view(request)

    assert response.status_code == 200


@pytest.mark.django_db
@pytest.mark.parametrize(
    'role_pk, status_code', [
        pytest.param(
            1, 200, marks=pytest.mark.success_request
        ),
        pytest.param(
            999, 404, marks=pytest.mark.bad_request
        )
    ]
)
def test_role_detail_view_without_exist_role(
        role_pk, status_code, api_factory, create_role
):
    create_role(pk=1, name='Test role')

    view = RoleDetailView.as_view()
    request = api_factory.get(reverse('api:accounts:role-detail', kwargs={'pk': role_pk}))
    response = view(request, pk=role_pk)

    assert response.status_code == status_code


@pytest.mark.django_db
def test_account_list_view(api_factory):
    view = AccountListView.as_view()
    request = api_factory.get(reverse('api:accounts:list'))
    response = view(request)

    assert response.status_code == 200


@pytest.mark.django_db
def test_account_me_view_with_authenticate(
        api_factory, create_user, get_token_for_user
):
    user = create_user()
    view = AccountMeView.as_view()
    request = api_factory.get(reverse('api:accounts:me-detail'))
    force_authenticate(request, user=user, token=get_token_for_user(user=user))
    response = view(request)

    assert response.status_code == 200


@pytest.mark.django_db
def test_account_me_view_without_authenticate(api_factory):
    view = AccountMeView.as_view()
    request = api_factory.get(reverse('api:accounts:me-detail'))
    response = view(request)

    assert response.status_code == 401


@pytest.mark.django_db
def test_account_me_update_display_role_view_with_authenticate(
        api_factory, create_user, get_token_for_user, create_role
):
    # Tworzymy usera
    user = create_user()

    # Tworzymy nowa role
    new_role = create_role(pk=80, name="Role 3")

    # Dodajemy userowi role
    user.roles.add(new_role)

    new_display_role = {
        'role': new_role.id
    }

    view = AccountMeUpdateDisplayRoleView.as_view()
    request = api_factory.put(reverse('api:accounts:me-update-display-role'), data=new_display_role)
    force_authenticate(request, user=user, token=get_token_for_user(user=user))
    response = view(request)

    assert response.status_code == 200


@pytest.mark.django_db
def test_account_me_display_role_view_without_authenticate(
        api_factory
):
    new_display_role = {
        'role': 999
    }

    view = AccountMeUpdateDisplayRoleView.as_view()
    request = api_factory.put(reverse('api:accounts:me-update-display-role'), data=new_display_role)
    response = view(request)

    assert response.status_code == 401


@pytest.mark.django_db
def test_account_me_wallet_list_view_with_authenticate(
        api_factory, create_user, get_token_for_user
):
    user = create_user()

    view = AccountMeWalletListView.as_view()
    request = api_factory.get(reverse('api:accounts:me-wallet-list'))
    force_authenticate(request, user=user, token=get_token_for_user(user=user))
    response = view(request)

    assert response.status_code == 200


@pytest.mark.django_db
def test_account_me_wallet_list_view_without_authenticate(
        api_factory
):
    view = AccountMeWalletListView.as_view()
    request = api_factory.get(reverse('api:accounts:me-wallet-list'))
    response = view(request)

    assert response.status_code == 401


@pytest.mark.django_db
def test_account_me_wallet_exchange_view_wallet_primary_without_authenticate(
        api_factory
):
    wtype = Wallet.WalletTypeChoices.PRIMARY

    view = AccountMeWalletExchangeView.as_view()
    request = api_factory.put(reverse('api:accounts:me-wallet-exchange', kwargs={'wtype': wtype}))
    response = view(request, wtype=wtype)

    assert response.status_code == 401


@pytest.mark.django_db
def test_account_me_wallet_exchange_view_wallet_secondary_without_authenticate(
        api_factory
):
    wtype = Wallet.WalletTypeChoices.SECONDARY

    view = AccountMeWalletExchangeView.as_view()
    request = api_factory.put(reverse('api:accounts:me-wallet-exchange', kwargs={'wtype': wtype}))
    response = view(request, wtype=wtype)

    assert response.status_code == 401


@pytest.mark.django_db
def test_account_me_wallet_exchange_view_wallet_secondary_with_channel_bonuscodes(
        api_factory, create_user, get_token_for_user, create_bonuscode
):
    user = create_user()
    bonus_code = create_bonuscode(code="TEST", money=Money(2, 'PLN'))
    wtype = Wallet.WalletTypeChoices.SECONDARY
    channel = PaymentMethod.PaymentChoices.CODE

    data = {
        'channel': channel,
        'code': bonus_code.code
    }

    view = AccountMeWalletExchangeView.as_view()
    request = api_factory.put(
        reverse('api:accounts:me-wallet-exchange', kwargs={'wtype': wtype}), data=data)
    force_authenticate(request, user=user, token=get_token_for_user(user=user))
    response = view(request, wtype=wtype)

    assert response.status_code == 200


@pytest.mark.django_db
def test_account_me_wallet_exchange_view_wallet_secondary_with_channel_sms(
        api_factory, create_user, get_token_for_user
):
    user = create_user()
    wtype = Wallet.WalletTypeChoices.SECONDARY
    channel = PaymentMethod.PaymentChoices.SMS

    data = {
        'channel': channel,
        'code': 'TEST'
    }

    view = AccountMeWalletExchangeView.as_view()
    request = api_factory.put(reverse('api:accounts:me-wallet-exchange', kwargs={'wtype': wtype}), data=data)
    force_authenticate(request, user=user, token=get_token_for_user(user=user))
    response = view(request, wtype=wtype)

    assert response.status_code == 400


@pytest.mark.django_db
def test_account_me_wallet_exchange_view_wallet_secondary_with_channel_transfer(
        api_factory, create_user, get_token_for_user
):
    user = create_user()
    wtype = Wallet.WalletTypeChoices.SECONDARY
    channel = PaymentMethod.PaymentChoices.TRANSFER

    data = {
        'channel': channel,
        'code': 'TEST'
    }

    view = AccountMeWalletExchangeView.as_view()
    request = api_factory.put(reverse('api:accounts:me-wallet-exchange', kwargs={'wtype': wtype}), data=data)
    force_authenticate(request, user=user, token=get_token_for_user(user=user))
    response = view(request, wtype=wtype)

    assert response.status_code == 400


"""
API CLIENT
"""


@pytest.mark.django_db
@pytest.mark.parametrize(
    'role_name, role_count, status_code', [
        pytest.param(
            'Test role', 1, 200,
            marks=pytest.mark.success_request
        ),
        pytest.param(
            None, 0, 200,
            marks=pytest.mark.success_request
        ),
    ]
)
def test_role_list_renders(
        role_name, role_count, status_code, api_client, create_role
):
    role = create_role(name='Test role')
    role_name = role.name

    response = api_client.get(reverse('api:accounts:role-list'))

    role_count = response.data['count']

    assert response.status_code == status_code


@pytest.mark.django_db
@pytest.mark.parametrize(
    'role_pk, status_code', [
        pytest.param(
            1, 200, marks=pytest.mark.success_request
        ),
        pytest.param(
            9999, 404, marks=pytest.mark.bad_request
        ),
    ]
)
def test_role_detail_renders(
        role_pk, status_code, create_role, api_client
):
    role = create_role(pk=1, name='Test role')

    response = api_client.get(reverse('api:accounts:role-detail', kwargs={'pk': role_pk}))
    assert response.status_code == status_code


@pytest.mark.django_db
@pytest.mark.parametrize(
    'account_count, status_code', [
        pytest.param(
            1, 200, marks=pytest.mark.success_request
        ),
        pytest.param(
            0, 200, marks=pytest.mark.success_request
        )
    ]
)
def test_account_list_renders(
        account_count, status_code, auto_login_user, api_client
):
    auto_login_user()

    response = api_client.get(reverse('api:accounts:list'))

    account_count = response.data['count']

    assert response.status_code == status_code


@pytest.mark.django_db()
def test_account_list_renders_filter_by_is_active(
        login_user, django_user_model, create_user, api_client
):
    second_steamid64 = '76561198145076068'

    login_user()

    # Tworzymy drugiego nie aktywnego uzytkownika
    create_user(steamid64=second_steamid64, is_active=False)

    url = reverse('api:accounts:list')
    response = api_client.get('{}?is_active={}'.format(url, 0))

    assert response.status_code == 200
    assert response.data['count'] == 1
    assert response.data['results'][0]['steamid64'] == second_steamid64


@pytest.mark.django_db
def test_account_list_renders_filter_by_display_role(
        create_user, create_role, api_client
):
    second_steamid64 = '76561198145076068'
    third_steamid64 = '76561198331043669'
    url = reverse('api:accounts:list')

    primary_user = create_user()
    secondary_user = create_user(steamid64=second_steamid64)
    thirty_user = create_user(steamid64=third_steamid64)

    new_role = create_role(pk=500, name='Test role')

    secondary_user.roles.add(new_role)
    secondary_user.update_display_role(new_role)

    thirty_user.roles.add(new_role)
    thirty_user.update_display_role(new_role)

    response = api_client.get('{}?display_role={}'.format(url, new_role.pk))

    assert response.status_code == 200
    assert response.data['count'] == 2


@pytest.mark.django_db
@pytest.mark.parametrize(
    'data, status_code', [
        pytest.param(
            qwizi_data, 200,
            marks=pytest.mark.success_request
        )
    ]
)
def test_account_me_renders_with_authenticate(
        data, status_code, api_client_with_credentials
):
    response = api_client_with_credentials.get(reverse('api:accounts:me-detail'))
    data = response.data
    assert response.status_code == status_code


@pytest.mark.django_db
def test_account_me_renders_without_authenticate(
        api_client
):
    response = api_client.get(reverse('api:accounts:me-detail'))

    assert response.status_code == 401


@pytest.mark.django_db
def test_account_me_update_display_role_without_authenticate(
        api_client
):
    response = api_client.put(reverse('api:accounts:me-update-display-role'))

    assert response.status_code == 401


@pytest.mark.django_db
def test_account_me_update_display_role_with_authenticate(
        login_user, qwizi_data, django_user_model, create_role, api_client_with_credentials
):
    login_user()
    user = django_user_model.objects.get(steamid64=qwizi_data['steamid64'])
    new_role = create_role(pk=3121, name="New role 2")
    user.roles.add(new_role)

    data = {
        'role': new_role.pk
    }
    response = api_client_with_credentials.put(reverse('api:accounts:me-update-display-role'), data=data)

    assert response.status_code == 200


@pytest.mark.django_db
def test_account_me_wallet_list_renders_without_authenticate(
        api_client
):
    response = api_client.get(reverse('api:accounts:me-wallet-list'))

    assert response.status_code == 401


@pytest.mark.django_db
def test_account_me_wallet_list_renders_with_authenticate(
        api_client_with_credentials
):
    response = api_client_with_credentials.get(reverse('api:accounts:me-wallet-list'))

    assert response.status_code == 200
    assert response.data['count'] == 2


@pytest.mark.django_db
@pytest.mark.parametrize(
    'wallet_type, channel, status_code', [
        pytest.param(
            Wallet.WalletTypeChoices.PRIMARY.value, PaymentMethod.PaymentChoices.CODE.value, 401,
        ),
        pytest.param(
            Wallet.WalletTypeChoices.SECONDARY.value, PaymentMethod.PaymentChoices.CODE.value, 401
        ),
        pytest.param(
            Wallet.WalletTypeChoices.OTHER.value, PaymentMethod.PaymentChoices.CODE.value, 401
        ),
    ]
)
def test_account_me_wallet_exchange_wallet_with_bonuscodes_without_authenticate(
        wallet_type, channel, status_code, api_client
):
    data = {
        'channel': channel,
        'code': 'Test'
    }

    url = reverse('api:accounts:me-wallet-exchange', kwargs={'wtype': wallet_type})

    response = api_client.put(url, data=data)

    assert response.status_code == status_code


@pytest.mark.django_db
@pytest.mark.parametrize(
    'wallet_type, channel, code, status_code', [
        pytest.param(
            Wallet.WalletTypeChoices.SECONDARY.value,
            PaymentMethod.PaymentChoices.CODE.value,
            'TEST',
            200
        ),
        pytest.param(
            Wallet.WalletTypeChoices.SECONDARY.value,
            PaymentMethod.PaymentChoices.CODE.value,
            'INVALID',
            400,
            marks=pytest.mark.bad_request
        ),
        pytest.param(
            Wallet.WalletTypeChoices.PRIMARY.value,
            PaymentMethod.PaymentChoices.CODE.value,
            'TEST',
            400,
            marks=pytest.mark.bad_request
        ),
    ]
)
def test_account_me_wallet_exchange_wallet_with_bonuscodes_with_authenticate(
        wallet_type, channel, code, status_code, create_bonuscode, api_client_with_credentials
):
    create_bonuscode(
        code="TEST",
        money=Money(2, 'PLN')
    )

    data = {
        'channel': channel,
        'code': code
    }

    url = reverse('api:accounts:me-wallet-exchange', kwargs={'wtype': wallet_type})

    response = api_client_with_credentials.put(url, data=data)

    assert response.status_code == status_code


"""
class AccountViewTestCase(AccountTestMixin):

    def setUp(self):
        super().setUp()
        self.account = Account.objects.create_user_steam(steamid64=self.steamid64)
        self.token = RefreshToken.for_user(self.account)

    def test_account_list_view(self):

        # Pobranie widoku dla listy uzytkownikow
        account_list_view = AccountListView.as_view()

        request = self.factory.get('/api/accounts/')
        response = account_list_view(request)

        self.assertEqual(response.status_code, 200)

    def test_account_me_view_with_authenticate(self):

        # Pobranie widoku dla danych zalogowanego uzytkownika
        view = AccountMeView.as_view()

        request = self.factory.get('/api/accounts/me/')

        # Zmuszamy uzytkownika do autoryzacji
        force_authenticate(request, user=self.account, token=self.token)

        response = view(request)
        self.assertEqual(response.status_code, 200)

    def test_account_me_view_without_authenticate(self):

        # Pobranie widoku dla danych nie zalogowanego uzytkownika
        view = AccountMeView.as_view()
        request = self.factory.get('/api/accounts/me/')
        response = view(request)

        self.assertEqual(response.status_code, 401)

    def test_account_me_update_display_role_view_with_authenticate(self):
        # Tworzymy nowa role
        new_role = Role.objects.create(name="New role")

        # Dodajemy nowa role do rol uzytkownika
        self.account.roles.add(new_role)

        new_display_role = {
            'role': new_role.pk
        }

        view = AccountMeUpdateDisplayRoleView.as_view()
        request = self.factory.put('/api/accounts/me/display-role/', data=new_display_role)
        force_authenticate(request, user=self.account, token=self.token)
        response = view(request)
        self.assertEqual(response.status_code, 200)

    def test_account_me_update_display_role_view_without_authenticate(self):
        # Tworzymy nowa role
        new_role = Role.objects.create(name="New role")

        # Dodajemy nowa role do rol uzytkownika
        self.account.roles.add(new_role)

        new_display_role = {
            'role': new_role.pk
        }

        view = AccountMeUpdateDisplayRoleView.as_view()
        request = self.factory.put('/api/accounts/me/display-role/', data=new_display_role)

        response = view(request)
        self.assertEqual(response.status_code, 401)

    def test_account_me_wallet_list_view_with_authenticate(self):
        view = AccountMeWalletListView.as_view()
        request = self.factory.get('/api/accounts/me/wallets/')
        force_authenticate(request, user=self.account, token=self.token)
        response = view(request)

        self.assertEqual(response.status_code, 200)

    def test_account_me_wallet_list_view_without_authenticate(self):
        view = AccountMeWalletListView.as_view()
        request = self.factory.get('/api/accounts/me/wallets/')
        response = view(request)

        self.assertEqual(response.status_code, 401)

    def test_role_list_view(self):

        view = RoleListView.as_view()
        request = self.factory.get('/api/accounts/roles/')
        response = view(request)

        self.assertEqual(response.status_code, 200)

    def test_role_detail_view(self):


        # Tworzymy przykladowa role
        role, created = Role.objects.get_or_create(name=self.user_role_name)

        view = RoleDetailView.as_view()
        request = self.factory.get('/api/accounts/roles/')
        response = view(request, pk=role.pk)

        self.assertEqual(response.status_code, 200)


class AccountViewApiTestCase(AccountTestMixin):
    def test_account_register(self):


        # Rejestracja domyslnego uzykownika
        self._login_user()

        # Pobieranie tego uzytkownika
        account = Account.objects.get(steamid64=self.steamid64)

        self.assertEqual(account.steamid64, self.steamid64)
        self.assertEqual(account.display_role.id, self.user_role_id)

    def test_account_login(self):


        # Rejestracja uzytkownika
        self._login_user()

        # Pobieranie zarejestrowanego uzytkownika

        account = Account.objects.get(steamid64=self.steamid64)

        # Logowanie uzytkownika
        self._login_user(account.steamid64)

        self.assertEqual(account.steamid64, self.steamid64)
        self.assertEqual(account.steamid32, self.steamid32)

    def test_account_login_invalid_steamid64(self):


        # Bledny steamid64
        steamid64 = "33234234"

        with self.assertRaises(Exception) as context:
            # Logowanie uzykownika
            self._login_user(steamid64)
        self.assertTrue("Invalid steamid64" in str(context.exception))

    def test_account_login_exists_username(self):


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

    def test_account_list_renders(self):

        # Steamid64 pierwszego uzytkownika
        steamid64_one = self.steamid64
        # Steamid64 drugiego uzytkownika
        steamid64_two = "76561198145076068"

        # Rejestrujemy pierwszego usera
        self._login_user(steamid64=steamid64_one)
        # Rejestrujemy drugiego usera
        self._login_user(steamid64=steamid64_two)

        response = self.client.get('/api/accounts/')

        # Pobieramy stworzonych uzytkownikow
        account_one_username = Account.objects.get(steamid64=steamid64_one)
        account_two_username = Account.objects.get(steamid64=steamid64_two)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['count'], 2)
        self.assertEqual(response.data['results'][0]['steamid64'], steamid64_one)
        self.assertEqual(response.data['results'][0]['display_role']['id'], self.user_role_id)
        self.assertEqual(response.data['results'][0]['formatted_username'], account_one_username.get_formatted_name())
        self.assertEqual(len(response.data['results'][0]['roles']), 1)
        self.assertEqual(response.data['results'][1]['steamid64'], steamid64_two)
        self.assertEqual(response.data['results'][1]['display_role']['id'], self.user_role_id)
        self.assertEqual(response.data['results'][1]['formatted_username'], account_two_username.get_formatted_name())
        self.assertEqual(len(response.data['results'][1]['roles']), 1)

    def test_account_list_renders_empty(self):

        response = self.client.get('/api/accounts/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['count'], 0)
        self.assertEqual(response.data['results'], [])

    def test_account_list_renders_filter_by_is_activate(self):


        # Tworzenie aktywnego konta
        activated_account = Account.objects.create_user_steam(steamid64=self.steamid64)

        # Tworzenie nie aktywnego konta
        deactivated_account = Account.objects.create_user_steam(steamid64="76561198188480002", is_active=False)

        first_response = self.client.get('/api/accounts/?is_active=1')

        self.assertEqual(first_response.status_code, 200)
        self.assertEqual(first_response.data['count'], 1)
        self.assertEqual(first_response.data['results'][0]['steamid64'], activated_account.steamid64)

        second_response = self.client.get('/api/accounts/?is_active=0')

        self.assertEqual(second_response.status_code, 200)
        self.assertEqual(second_response.data['count'], 1)
        self.assertEqual(second_response.data['results'][0]['steamid64'], deactivated_account.steamid64)

    def test_account_list_renders_filter_by_display_role(self):


        # Tworzenie konta z rola User
        user_account = Account.objects.create_user_steam(steamid64=self.steamid64)

        # Tworzenie konta z rola Admin
        admin_account = Account.objects.create_superuser_steam(steamid64="76561198188480002")

        first_response = self.client.get('/api/accounts/?display_role={}'.format(user_account.display_role.id))

        self.assertEqual(first_response.status_code, 200)
        self.assertEqual(first_response.data['count'], 1)
        self.assertEqual(first_response.data['results'][0]['display_role']['id'], user_account.display_role.id)

        second_response = self.client.get('/api/accounts/?display_role={}'.format(admin_account.display_role.id))

        self.assertEqual(second_response.status_code, 200)
        self.assertEqual(second_response.data['count'], 1)
        self.assertEqual(second_response.data['results'][0]['display_role']['id'], admin_account.display_role.id)

    def test_account_me_renders_with_authenticate(self):


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
        self.assertEqual(response.data['formatted_username'], account.get_formatted_name())
        self.assertEqual(response.data['display_role']['id'], self.user_role_id)
        self.assertEqual(response.data['threads'], 0)
        self.assertEqual(response.data['posts'], 0)

    def test_account_me_renders_count_threads_with_authenticate(self):


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

    def test_account_me_renders_count_posts_with_authenticate(self):


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

    def test_account_me_renders_without_authenticate(self):

        response = self.client.get('/api/accounts/me/')
        self.assertEqual(response.status_code, 401)

    def test_account_me_update_display_role_renders_with_authenticate(self):


        # Rejestrujemy domyslnego uzytkownika
        self._login_user()

        # Pobieramy uzytkonwika
        account = Account.objects.get(steamid64=self.steamid64)

        # Pobieramy token dla uzykownika
        token = self._get_token(account)

        # Ustawawiamy headery dla autoryzacji
        self._create_credentials(token)

        # Tworzymy nowa role
        new_role = Role.objects.create(name="New role")

        # Dodajemy nowa role do rol uzytkownika
        account.roles.add(new_role)

        new_display_role = {
            'role': new_role.pk
        }

        response = self.client.put('/api/accounts/me/display-role/', data=new_display_role)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['display_role'], new_role.pk)

    def test_account_me_update_display_role_renders_with_authenticate_not_exist_role(self):


        # Rejestrujemy domyslnego uzytkownika
        self._login_user()

        # Pobieramy uzytkonwika
        account = Account.objects.get(steamid64=self.steamid64)

        # Pobieramy token dla uzykownika
        token = self._get_token(account)

        # Ustawawiamy headery dla autoryzacji
        self._create_credentials(token)

        # Id nie istniejaccej roli
        invalid_role = 999

        new_display_role = {
            'role': invalid_role
        }

        response = self.client.put('/api/accounts/me/display-role/', data=new_display_role)

        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.data['msg'], 'Podana rola nie istnieje')

    def test_account_me_wallet_list_renders_with_authenticate(self):
        # Rejestrujemy domyslnego uzytkownika
        self._login_user()

        # Pobieramy uzytkonwika
        account = Account.objects.get(steamid64=self.steamid64)

        # Pobieramy token dla uzykownika
        token = self._get_token(account)

        # Ustawawiamy headery dla autoryzacji
        self._create_credentials(token)

        response = self.client.get('/api/accounts/me/wallets/')

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['count'], 2)

    def test_account_me_wallet_list_renders_empty_with_authenticated(self):
        # Rejestrujemy domyslnego uzytkownika
        self._login_user()

        # Pobieramy uzytkonwika
        account = Account.objects.get(steamid64=self.steamid64)

        # Usuwamy portfele
        for wallet in account.wallet_set.all():
            wallet.delete()

        # Pobieramy token dla uzykownika
        token = self._get_token(account)

        # Ustawawiamy headery dla autoryzacji
        self._create_credentials(token)

        response = self.client.get('/api/accounts/me/wallets/')

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['count'], 0)

    def test_account_me_wallet_list_renders_filer_by_wtype(self):
        # Rejestrujemy domyslnego uzytkownika
        self._login_user()

        # Pobieramy uzytkonwika
        account = Account.objects.get(steamid64=self.steamid64)

        # Pobieramy token dla uzykownika
        token = self._get_token(account)

        # Ustawawiamy headery dla autoryzacji
        self._create_credentials(token)

        first_response = self.client.get('/api/accounts/me/wallets/')

        self.assertEqual(first_response.status_code, 200)
        self.assertEqual(first_response.data['count'], 2)

        PRIMARY = Wallet.WalletTypeChoices.PRIMARY
        SECONDARY = Wallet.WalletTypeChoices.SECONDARY
        OTHER = Wallet.WalletTypeChoices.OTHER

        second_response = self.client.get('/api/accounts/me/wallets/?wtype={}'.format(PRIMARY))

        self.assertEqual(second_response.status_code, 200)
        self.assertEqual(second_response.data['count'], 1)
        self.assertEqual(second_response.data['results'][0]['wtype'], PRIMARY)

        third_response = self.client.get('/api/accounts/me/wallets/?wtype={}'.format(SECONDARY))

        self.assertEqual(third_response.status_code, 200)
        self.assertEqual(third_response.data['count'], 1)
        self.assertEqual(third_response.data['results'][0]['wtype'], SECONDARY)

        fourth_response = self.client.get('/api/accounts/me/wallets/?wtype={}'.format(OTHER))

        self.assertEqual(fourth_response.status_code, 200)
        self.assertEqual(fourth_response.data['count'], 0)

    def test_account_me_wallet_secondary_exchange_bonusodes_valid_code_renders_with_authenticate(self):
        # Rejestrujemy domyslnego uzytkownika
        self._login_user()

        # Pobieramy uzytkonwika
        account = Account.objects.get(steamid64=self.steamid64)

        # Kod
        code = "TEST"
        # Ilosc gotowki
        money = Money(2, 'PLN')

        # Tworzymy bonusowy kod
        BonusCode.objects.create(
            code=code,
            money=money
        )

        # Sprawdzanie czy drugi porfel uzytkownika nie posiada srodkow
        secondary_wallet = account.wallet_set.get(wtype=Wallet.WalletTypeChoices.SECONDARY)
        secondary_wallet_channel = secondary_wallet.payment_methods.get(name=PaymentMethod.PaymentChoices.CODE)
        self.assertEqual(secondary_wallet.money, Money(0, 'PLN'))

        # Pobieramy token dla uzykownika
        token = self._get_token(account)

        # Ustawawiamy headery dla autoryzacji
        self._create_credentials(token)

        # Dane ktore zostana wyslane na endpoint
        data = {
            'channel': secondary_wallet_channel.name,
            'code': code
        }
        response = self.client.put('/api/accounts/me/wallets/{}/'.format(secondary_wallet.wtype), data=data)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(account.wallet_set.get(wtype=Wallet.WalletTypeChoices.SECONDARY).money, Money(2, 'PLN'))

    def test_account_me_wallet_secondary_exchange_bonuscodes_invalid_code_renders_with_authenticate(self):
        # Rejestrujemy domyslnego uzytkownika
        self._login_user()

        # Pobieramy uzytkonwika
        account = Account.objects.get(steamid64=self.steamid64)

        # Kod
        code = "TEST"
        # Ilosc gotowki
        money = Money(2, 'PLN')

        # Sprawdzanie czy drugi porfel uzytkownika nie posiada srodkow
        secondary_wallet = account.wallet_set.get(wtype=Wallet.WalletTypeChoices.SECONDARY)
        secondary_wallet_channel = secondary_wallet.payment_methods.get(name=PaymentMethod.PaymentChoices.CODE)
        self.assertEqual(secondary_wallet.money, Money(0, 'PLN'))

        # Pobieramy token dla uzykownika
        token = self._get_token(account)

        # Ustawawiamy headery dla autoryzacji
        self._create_credentials(token)

        # Dane ktore zostana wyslane na endpoint
        data = {
            'channel': secondary_wallet_channel.name,
            'code': code
        }
        response = self.client.put('/api/accounts/me/wallets/{}/'.format(secondary_wallet.wtype), data=data)

        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.data[0], "Podany kod jest niepoprawny")

    def test_account_me_wallet_secondary_exchange_invalid_channel_bonuscodes_renders_with_authenticate(self):
        # Rejestrujemy domyslnego uzytkownika
        self._login_user()

        # Pobieramy uzytkonwika
        account = Account.objects.get(steamid64=self.steamid64)

        # Kod
        code = "TEST"
        # Ilosc gotowki
        money = Money(2, 'PLN')

        # Tworzymy bonusowy kod
        BonusCode.objects.create(
            code=code,
            money=money
        )

        # Sprawdzanie czy drugi porfel uzytkownika nie posiada srodkow
        secondary_wallet = account.wallet_set.get(wtype=Wallet.WalletTypeChoices.SECONDARY)
        # secondary_wallet_channel = secondary_wallet.payment_methods.get(name=PaymentMethod.PaymentChoices.SMS)
        self.assertEqual(secondary_wallet.money, Money(0, 'PLN'))

        # Pobieramy token dla uzykownika
        token = self._get_token(account)

        # Ustawawiamy headery dla autoryzacji
        self._create_credentials(token)

        # Dane ktore zostana wyslane na endpoint
        data = {
            'channel': PaymentMethod.PaymentChoices.SMS,
            'code': code
        }
        response = self.client.put('/api/accounts/me/wallets/{}/'.format(secondary_wallet.wtype), data=data)
        print(response.data)
        self.assertEqual(response.status_code, 400)

    def test_role_list_renders(self):


        second_role_name = 'Druga rola'

        Role.objects.create(name=self.user_role_name)
        Role.objects.create(name=second_role_name)

        response = self.client.get('/api/accounts/roles/')

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['count'], 2)
        self.assertEqual(response.data['results'][0]['name'], self.user_role_name)
        self.assertEqual(response.data['results'][1]['name'], second_role_name)

    def test_role_list_renders_empty(self):


        response = self.client.get('/api/accounts/roles/')

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['count'], 0)

    def test_role_detail_renders(self):


        # Tworzymy role
        role = Role.objects.create(name=self.user_role_name)

        response = self.client.get('/api/accounts/roles/{}/'.format(role.id))

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['name'], role.name)
        self.assertEqual(response.data['format'], role.format)

    def test_role_detail_renders_not_exist(self):
        invalid_role = 999

        response = self.client.get('/api/accounts/roles/{}/'.format(invalid_role))

        self.assertEqual(response.status_code, 404)
"""
