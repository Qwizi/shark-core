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
    AccountMeWalletExchangeView,
    AdminAccountViewSet,

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
@pytest.mark.parametrize(
    'code, wallet_type, channel, status_code', [
        # PARAMSY DLA DODATKOWEGO PORTFELA
        pytest.param(
            'SHARK500', Wallet.WalletTypeChoices.SECONDARY.value, PaymentMethod.PaymentChoices.CODE.value, 200,
            marks=pytest.mark.success_request
        ),
        pytest.param(
            'TEST0000', Wallet.WalletTypeChoices.SECONDARY.value, PaymentMethod.PaymentChoices.CODE.value, 400,
            marks=pytest.mark.bad_request
        ),
        pytest.param(
            'TEST0000', Wallet.WalletTypeChoices.SECONDARY.value, PaymentMethod.PaymentChoices.SMS.value, 400,
            marks=pytest.mark.bad_request
        ),
        pytest.param(
            'TEST0000', Wallet.WalletTypeChoices.SECONDARY.value, PaymentMethod.PaymentChoices.TRANSFER.value, 400,
            marks=pytest.mark.skip
        ),
        # PARAMSY DLA PODSTAWOWEGO PORTFELAd
        pytest.param(
            # Prawidlowy testowy kod liveserver
            'TEST0001', Wallet.WalletTypeChoices.PRIMARY.value, PaymentMethod.PaymentChoices.SMS.value, 200,
            marks=pytest.mark.success_request
        ),
        pytest.param(
            'TEST0000', Wallet.WalletTypeChoices.PRIMARY.value, PaymentMethod.PaymentChoices.SMS.value, 400,
            marks=pytest.mark.bad_request
        ),
        pytest.param(
            'TEST0000', Wallet.WalletTypeChoices.PRIMARY.value, PaymentMethod.PaymentChoices.CODE.value, 400,
            marks=pytest.mark.bad_request
        ),
        pytest.param(
            'TEST0000', Wallet.WalletTypeChoices.PRIMARY.value, PaymentMethod.PaymentChoices.TRANSFER.value, 400,
            marks=pytest.mark.skip
        ),
    ]
)
def test_account_me_wallet_exchange_view_with_authenticate(
        code, wallet_type, channel, status_code, api_factory, create_user, get_token_for_user, create_bonuscode
):
    user = create_user()
    create_bonuscode(code="SHARK500", money=Money(2, 'PLN'))

    data = {
        'channel': channel,
        'code': code
    }

    view = AccountMeWalletExchangeView.as_view()
    request = api_factory.put(
        reverse('api:accounts:me-wallet-exchange', kwargs={'wtype': wallet_type}), data=data)
    force_authenticate(request, user=user, token=get_token_for_user(user=user))
    response = view(request, wtype=wallet_type)

    assert response.status_code == status_code


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


@pytest.mark.django_db
@pytest.mark.parametrize(
    'http, method, status_code', [
        pytest.param(
            'get', 'list', 401
        ),
        pytest.param(
            'post', 'create', 401
        ),
        pytest.param(
            'get', 'retrieve', 401
        ),
        pytest.param(
            'put', 'update', 401
        ),
        pytest.param(
            'delete', 'destroy', 401
        )
    ]
)
def test_admin_account_view_without_authenticate(
        http, method, status_code, api_factory
):
    view = AdminAccountViewSet.as_view({'{}'.format(http): method})
    request = None
    if http == 'get':
        if method == 'list':
            url = reverse('api:adminapi:accounts:list')
            request = api_factory.get(url)
        else:
            url = reverse('api:adminapi:accounts:detail', kwargs={'pk': 9999})
            request = api_factory.get(url)
    elif http == 'post':
        url = reverse('api:adminapi:accounts:list')
        request = api_factory.post(url)
    elif http == 'put':
        url = reverse('api:adminapi:accounts:detail', kwargs={'pk': 999})
        request = api_factory.put(url)
    elif http == 'delete':
        url = reverse('api:adminapi:accounts:detail', kwargs={'pk': 999})
        request = api_factory.delete(url)

    response = view(request)

    assert response.status_code == status_code


@pytest.mark.django_db
@pytest.mark.parametrize(
    'http, method, status_code', [
        pytest.param(
            'get', 'list', 403
        ),
        pytest.param(
            'post', 'create', 403
        ),
        pytest.param(
            'get', 'retrieve', 403
        ),
        pytest.param(
            'put', 'update', 403
        ),
        pytest.param(
            'delete', 'destroy', 403
        )
    ]
)
def test_admin_account_view_without_permissions(
        http, method, status_code, api_factory, create_user, get_token_for_user
):
    user = create_user()

    view = AdminAccountViewSet.as_view({'{}'.format(http): method})
    request = None
    if http == 'get':
        if method == 'list':
            url = reverse('api:adminapi:accounts:list')
            request = api_factory.get(url)
        else:
            url = reverse('api:adminapi:accounts:detail', kwargs={'pk': 9999})
            request = api_factory.get(url)
    elif http == 'post':
        url = reverse('api:adminapi:accounts:list')
        request = api_factory.post(url)
    elif http == 'put':
        url = reverse('api:adminapi:accounts:detail', kwargs={'pk': 999})
        request = api_factory.put(url)
    elif http == 'delete':
        url = reverse('api:adminapi:accounts:detail', kwargs={'pk': 999})
        request = api_factory.delete(url)

    force_authenticate(request, user=user, token=get_token_for_user(user=user))
    response = view(request)

    assert response.status_code == status_code


@pytest.mark.django_db
def test_admin_account_list_view(
        api_factory, create_superuser, get_token_for_user
):
    user = create_superuser()

    view = AdminAccountViewSet.as_view({'get': 'list'})
    request = api_factory.get(reverse('api:adminapi:accounts:list'))
    force_authenticate(request, user=user, token=get_token_for_user(user=user))
    response = view(request)

    assert response.status_code == 200


@pytest.mark.django_db
@pytest.mark.parametrize(
    'acccount_id, status_code', [
        pytest.param(
            1, 200
        ),
        pytest.param(
            999, 404
        )
    ]
)
def test_admin_account_detail_view(
        acccount_id, status_code, api_factory, create_superuser, get_token_for_user
):
    user = create_superuser(pk=1)

    view = AdminAccountViewSet.as_view({'get': 'retrieve'})
    request = api_factory.get(reverse('api:adminapi:accounts:detail', kwargs={'pk': acccount_id}))
    force_authenticate(request, user=user, token=get_token_for_user(user=user))
    response = view(request, pk=acccount_id)

    assert response.status_code == status_code


@pytest.mark.django_db
@pytest.mark.parametrize(
    'account_id, status_code', [
        pytest.param(
            1, 204
        ),
        pytest.param(
            999, 404
        )
    ]
)
def test_admin_account_delete_view(
        account_id, status_code, api_factory, create_superuser, get_token_for_user
):
    user = create_superuser(pk=1)

    view = AdminAccountViewSet.as_view({'delete': 'destroy'})
    request = api_factory.delete(reverse('api:adminapi:accounts:detail', kwargs={'pk': account_id}))
    force_authenticate(request, user=user, token=get_token_for_user(user=user))
    response = view(request, pk=account_id)

    assert response.status_code == status_code


@pytest.mark.skip
@pytest.mark.django_db
@pytest.mark.parametrize(
    'account_id, new_username, status_code', [
        pytest.param(
            1, 'Qwizi2', 202
        ),
        pytest.param(
            999, None, 404
        )
    ]

)
def test_admin_account_update_view(
        account_id, new_username, status_code, api_factory, create_superuser, get_token_for_user
):
    user = create_superuser(pk=1)

    data = {
        'username': 'Qwizi2'
    }

    view = AdminAccountViewSet.as_view({'put': 'update'})
    request = api_factory.put(reverse('api:adminapi:accounts:detail', kwargs={'pk': account_id}), data=data)
    force_authenticate(request, user=user, token=get_token_for_user(user=user))
    response = view(request, pk=account_id)

    assert response.data == 2
    assert response.status_code == status_code
    if response.status_code == 200:
        assert response.data['username'] == new_username


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
            '76561198190469450', 200,
            marks=pytest.mark.success_request
        )
    ]
)
def test_account_me_renders_with_authenticate(
        data, status_code, api_client_with_credentials
):
    response = api_client_with_credentials.get(reverse('api:accounts:me-detail'))

    assert response.status_code == status_code
    assert response.data['steamid64'] == data


@pytest.mark.django_db
def test_account_me_renders_without_authenticate(
        api_client
):
    response = api_client.get(reverse('api:accounts:me-detail'))

    assert response.status_code == 401


@pytest.mark.django_db
def test_account_me_update_display_role_renders_without_authenticate(
        api_client
):
    response = api_client.put(reverse('api:accounts:me-update-display-role'))

    assert response.status_code == 401


@pytest.mark.django_db
def test_account_me_update_display_role_renders_with_authenticate(
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
def test_account_me_wallet_exchange_renders_without_authenticate(
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
    'code, wallet_type, channel, money, status_code', [
        # PARAMSY DLA DODATKOWEGO PORTFELA
        pytest.param(
            'SHARK500',
            Wallet.WalletTypeChoices.SECONDARY.value,
            PaymentMethod.PaymentChoices.CODE.value,
            Money(2, 'PLN'),
            200,
            marks=pytest.mark.success_request
        ),
        pytest.param(
            'TEST0000',
            Wallet.WalletTypeChoices.SECONDARY.value,
            PaymentMethod.PaymentChoices.CODE.value,
            None,
            400,
            marks=pytest.mark.bad_request
        ),
        pytest.param(
            'TEST0000',
            Wallet.WalletTypeChoices.SECONDARY.value,
            PaymentMethod.PaymentChoices.SMS.value,
            None,
            400,
            marks=pytest.mark.bad_request
        ),
        pytest.param(
            'TEST0000',
            Wallet.WalletTypeChoices.SECONDARY.value,
            PaymentMethod.PaymentChoices.TRANSFER.value,
            None,
            400,
            marks=pytest.mark.skip
        ),
        # PARAMSY DLA PODSTAWOWEGO PORTFELAd
        pytest.param(
            # Prawidlowy testowy kod liveserver
            'TEST0001',
            Wallet.WalletTypeChoices.PRIMARY.value,
            PaymentMethod.PaymentChoices.SMS.value,
            Money(5, 'PLN'),
            200,
            marks=pytest.mark.success_request
        ),
        pytest.param(
            'TEST0000',
            Wallet.WalletTypeChoices.PRIMARY.value,
            PaymentMethod.PaymentChoices.SMS.value,
            None,
            400,
            marks=pytest.mark.bad_request
        ),
        pytest.param(
            'TEST0000',
            Wallet.WalletTypeChoices.PRIMARY.value,
            PaymentMethod.PaymentChoices.CODE.value,
            None,
            400,
            marks=pytest.mark.bad_request
        ),
        pytest.param(
            'TEST0000',
            Wallet.WalletTypeChoices.PRIMARY.value,
            PaymentMethod.PaymentChoices.TRANSFER.value,
            None,
            400,
            marks=pytest.mark.skip
        ),
    ]
)
def test_account_me_wallet_exchange_wallet_renders_with_authenticate(
        code, wallet_type, channel, money, status_code, create_bonuscode, api_client_with_credentials
):
    create_bonuscode(
        code="SHARK500",
        money=Money(2, 'PLN')
    )

    data = {
        'channel': channel,
        'code': code
    }

    url = reverse('api:accounts:me-wallet-exchange', kwargs={'wtype': wallet_type})

    response = api_client_with_credentials.put(url, data=data)

    assert response.status_code == status_code
    if status_code == 200:
        response_money = Money(response.data['money'], 'PLN')
        assert response_money == money


@pytest.mark.django_db
def test_admin_accounts_list_renders(
        api_client_with_credentials
):
    response = api_client_with_credentials.get(reverse('api:adminapi:accounts:list'))

    assert response.status_code == 200


@pytest.mark.django_db
@pytest.mark.parametrize(
    'account_id, status_code', [
        pytest.param(
            50, 200
        ),
        pytest.param(
            999, 404
        )
    ]
)
def test_admin_accounts_detail_renders(
        account_id, status_code, api_client_with_credentials, create_user
):
    user = create_user(pk=50, force=True)

    response = api_client_with_credentials.get(reverse('api:adminapi:accounts:detail', kwargs={'pk': account_id}))
    assert response.status_code == status_code


@pytest.mark.django_db
@pytest.mark.parametrize(
    'account_id, status_code', [
        pytest.param(
            50, 204
        ),
        pytest.param(
            999, 404
        )
    ]
)
def test_admin_accounts_delete_renders(
        account_id, status_code, api_client_with_credentials, create_user
):
    user = create_user(pk=50, force=True)

    response = api_client_with_credentials.delete(reverse('api:adminapi:accounts:detail', kwargs={'pk': account_id}))

    assert response.status_code == status_code
