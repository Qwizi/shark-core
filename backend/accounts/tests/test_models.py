import pytest
from .fixtures import *


@pytest.mark.django_db
@pytest.mark.parametrize(
    'name, count', [
        pytest.param(
            'Role 1', 1, marks=pytest.mark.success_request
        ),
    ]
)
def test_role_create(
        name, count, create_role
):
    role = create_role(name="Role 1")

    assert role.name == name
    assert Role.objects.all().count() == count


@pytest.mark.django_db
@pytest.mark.parametrize(
    'role_format', [
        pytest.param(
            default_role_format, marks=pytest.mark.success_request
        )
    ]
)
def test_role_create_random_color_format(
        role_format, create_role
):
    role = create_role(name="Role 2")
    role.create_random_color_format()

    assert role.format != role_format


@pytest.mark.django_db
def test_account_create_user_steam_with_valid_steamid64(
        django_user_model, create_user, qwizi_data
):
    account = create_user()

    assert django_user_model.objects.all().count() == 1
    assert account.steamid64 == qwizi_data['steamid64']
    assert account.steamid32 == qwizi_data['steamid32']
    assert account.steamid3 == qwizi_data['steamid3']
    assert account.username == qwizi_data['username']
    assert account.avatar == qwizi_data['avatar']
    assert account.avatarmedium == qwizi_data['avatarmedium']
    assert account.avatarfull == qwizi_data['avatarfull']
    assert account.loccountrycode == qwizi_data['loccountrycode']


@pytest.mark.django_db
def test_account_create_user_steam_with_invalid_steamid64(create_user):
    invalid_steamid64 = "12312112321"

    with pytest.raises(Exception) as context:
        create_user(steamid64=invalid_steamid64)
    assert "Invalid steamid64" in str(context.value)


@pytest.mark.django_db
def test_account_create_superuser_steam_with_valid_steamid64(create_superuser, qwizi_data):
    admin_account = create_superuser()

    assert admin_account.steamid64 == qwizi_data['steamid64']


@pytest.mark.django_db
def test_account_create_user_steam_with_none_steamid64(create_user):
    steamid64 = None

    with pytest.raises(Exception) as context:
        create_user(steamid64=steamid64)
    assert "Steamid64 cannot be None" in str(context.value)


@pytest.mark.django_db
def test_account_activate(create_user):
    deactivated_account = create_user(is_active=False)

    deactivated_account.activate()

    assert deactivated_account.is_active is True


@pytest.mark.django_db
def test_account_get_formatted_name(create_user, default_user_role_format):
    account = create_user()

    formatted_name = default_user_role_format.replace('{username}', account.username)

    assert account.get_formatted_name() == formatted_name


@pytest.mark.django_db
def test_account_update_display_role(create_user, create_role):
    account = create_user()
    # Tworzymy nowa role
    new_role = create_role(pk=99, name="Role 3")
    # Dodajemy role do konta
    account.roles.add(new_role)

    account.update_display_role(new_role)

    assert account.display_role == new_role


@pytest.mark.django_db
def test_account_on_created_wallets_exist(create_user):
    account = create_user()

    assert account.wallet_set.all().count() == 2
    assert account.wallet_set.all()[0].wtype == Wallet.WalletTypeChoices.PRIMARY
    assert account.wallet_set.all()[1].wtype == Wallet.WalletTypeChoices.SECONDARY


@pytest.mark.django_db
def test_paymentmethod_create_with_code_name(create_paymentmethod):
    create_paymentmethod(name=PaymentMethod.PaymentChoices.CODE)

    assert PaymentMethod.objects.all().count() == 1


@pytest.mark.django_db
def test_paymentmethod_create_with_sms_name(create_paymentmethod):
    create_paymentmethod(name=PaymentMethod.PaymentChoices.SMS)

    assert PaymentMethod.objects.all().count() == 1


@pytest.mark.django_db
def test_paymentmethod_create_with_transfer_name(create_paymentmethod):
    create_paymentmethod(name=PaymentMethod.PaymentChoices.TRANSFER)

    assert PaymentMethod.objects.all().count() == 1


@pytest.mark.django_db
def test_wallet_create(create_user, create_wallet):
    account = create_user()
    create_wallet(
        wtype=Wallet.WalletTypeChoices.OTHER,
        account=account
    )

    assert Wallet.objects.all().count() == 3


@pytest.mark.django_db
def test_wallet_add_money(create_user):
    account = create_user()
    wallet = account.wallet_set.get(wtype=Wallet.WalletTypeChoices.PRIMARY)
    money_to_add = Money(10, 'PLN')
    wallet.add_money(money_to_add)

    assert wallet.money == money_to_add


@pytest.mark.django_db
def test_wallet_subtract_money(create_user):
    account = create_user()

    wallet = account.wallet_set.get(wtype=Wallet.WalletTypeChoices.PRIMARY)
    wallet.money = Money(20, 'PLN')
    wallet.save()

    money_to_subtract = Money(10, 'PLN')
    wallet.subtract_money(money_to_subtract)

    assert wallet.money == Money(10, 'PLN')


@pytest.mark.django_db
def test_bonuscode_create(create_bonuscode):
    create_bonuscode(
        code="TEST",
        money=Money(5, 'PLN')
    )

    assert BonusCode.objects.all().count() == 1


@pytest.mark.django_db
def test_smsnumber_create(create_smsnumber):
    create_smsnumber(
        provider="test",
        number=7777,
        expanse=Money(5, 'PLN'),
        money=Money(2.50, 'PLN')
    )

    assert SMSNumber.objects.all().count() == 1
