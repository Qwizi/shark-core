from pytest import fixture

from ..models import (
    Role,
    Wallet,
    BonusCode,
    SMSNumber,
    PaymentMethod
)

from steambot.models import (
    Queue
)

from djmoney.money import Money

from ..providers import payment_manager
from ..steam_helpers import get_steam_user_info

from rest_framework.test import force_authenticate


@fixture
def get_token_for_user(create_user):
    def get_token(**kwargs):
        from rest_framework_simplejwt.tokens import RefreshToken
        if "user" not in kwargs:
            kwargs['user'] = create_user()

        return RefreshToken.for_user(kwargs['user'])

    return get_token


@fixture
def api_factory():
    from rest_framework.test import APIRequestFactory
    return APIRequestFactory()


@fixture
def api_client():
    from rest_framework.test import APIClient
    return APIClient()


@fixture
def api_client_with_credentials(
        db, create_user, api_client, get_token_for_user
):
    user = create_user()
    token = get_token_for_user(user=user)
    api_client.force_authenticate(user=user, token=token)
    yield api_client
    api_client.force_authenticate(user=None)


@fixture
def qwizi_data():
    return {
        'steamid64': '76561198190469450',
        'steamid32': 'STEAM_1:0:115101861',
        'steamid3': '[U:1:230203722]',
        'username': 'Qwizi',
        'avatar': 'https://steamcdn-a.akamaihd.net/steamcommunity/public/images/avatars/35/35f3a0e0d3f895f4ae608ccf68ae4e7b262a544d.jpg',
        'avatarmedium': 'https://steamcdn-a.akamaihd.net/steamcommunity/public/images/avatars/35/35f3a0e0d3f895f4ae608ccf68ae4e7b262a544d_medium.jpg',
        'avatarfull': 'https://steamcdn-a.akamaihd.net/steamcommunity/public/images/avatars/35/35f3a0e0d3f895f4ae608ccf68ae4e7b262a544d_full.jpg',
        'loccountrycode': 'PL',
        'profileurl': 'https://steamcommunity.com/id/34534645645/',
        'tradeurl': 'https://steamcommunity.com/tradeoffer/new/?partner=230203722&token=7HI_fhSK'
    }


@fixture
def create_user(db, django_user_model, qwizi_data):
    def make_user(**kwargs):
        if "steamid64" not in kwargs:
            kwargs['steamid64'] = qwizi_data['steamid64']
        if "tradeurl" not in kwargs:
            kwargs['tradeurl'] = qwizi_data['tradeurl']

        return django_user_model.objects.create_user_steam(**kwargs)

    return make_user


@fixture
def create_superuser(db, django_user_model, qwizi_data):
    def make_user(**kwargs):
        if "steamid64" not in kwargs:
            kwargs['steamid64'] = qwizi_data['steamid64']
        if "tradeurl" not in kwargs:
            kwargs['tradeurl'] = qwizi_data['tradeurl']

        return django_user_model.objects.create_superuser_steam(**kwargs)

    return make_user


@fixture
def auto_login_user(db, client, qwizi_data):
    def make_auto_login(steamid64=None):
        if steamid64 is None:
            steamid64 = qwizi_data['steamid64']
        client.login(steamid64=steamid64)

    return make_auto_login


@fixture
def login_user(db, api_client, qwizi_data):
    def make_login(steamid64=None):
        if steamid64 is None:
            steamid64 = qwizi_data['steamid64']
        api_client.login(steamid64=steamid64)

    return make_login


@fixture
def default_role_format():
    return '{username}'


@fixture
def default_user_role_format():
    return '<span color="rgb(113,118,114)">{username}</span>'


@fixture
def default_admin_role_format():
    return '<span color="rgb(242,0,0)">{username}</span>'


@fixture
def create_role(db):
    def make_role(**kwargs):
        return Role.objects.create(**kwargs)

    return make_role


@fixture
def create_wallet(db):
    def make_wallet(**kwargs):
        return Wallet.objects.create(**kwargs)

    return make_wallet


@fixture
def create_bonuscode(db):
    def make_bonuscode(**kwargs):
        return BonusCode.objects.create(**kwargs)

    return make_bonuscode


@fixture
def create_smsnumber(db):
    def make_smsnumber(**kwargs):
        return SMSNumber.objects.create(**kwargs)

    return make_smsnumber


@fixture
def create_paymentmethod(db):
    def make_paymentmethod(**kwargs):
        return PaymentMethod.objects.create(**kwargs)

    return make_paymentmethod


@fixture
def create_queue(db):
    def make_queue(**kwargs):
        return Queue.objects.create(**kwargs)

    return make_queue
