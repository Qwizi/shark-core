from pytest import fixture

from ..models import (
    Role,
    Wallet,
    BonusCode,
    SMSNumber,
    PaymentMethod
)

from djmoney.money import Money

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
        'loccountrycode': 'PL'
    }


@fixture
def create_user(db, django_user_model, qwizi_data):
    def make_user(**kwargs):
        if "steamid64" not in kwargs:
            kwargs['steamid64'] = qwizi_data['steamid64']
        return django_user_model.objects.create_user_steam(**kwargs)

    return make_user


@fixture
def create_superuser(db, django_user_model, qwizi_data):
    def make_user(**kwargs):
        if "steamid64" not in kwargs:
            kwargs['steamid64'] = qwizi_data['steamid64']
        return django_user_model.objects.create_superuser_steam(**kwargs)

    return make_user


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
