from pytest import fixture

from ..models import (
    Role,
    Wallet,
    BonusCode,
    SMSNumber,
    PaymentMethod
)
from forum.models import (
    SubCategory,
    Category,
    Thread,
    Post,
    ReactionItem,
    Reaction,

)

from steambot.models import (
    Queue
)

from store.models import (
    Group,
    Item,
    History,
    VipCache
)

from servers.models import (
    Game,
    Server,
)

from news.models import News

from django.core.files import File
from django.core.files.temp import NamedTemporaryFile
from djmoney.money import Money

import requests

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
        db, create_superuser, api_client, get_token_for_user
):
    user = create_superuser()
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
        'loccountrycode': 'PL',
    }


@fixture
def create_user(db, django_user_model, qwizi_data):
    def make_user(**kwargs):
        force = None

        """
        Sprawdzamy czy force jest ustawiony jezeli tak usuwamy wartosc ze slownika
        i wrzucamy wartosc do zmiennej
        """
        if "force" in kwargs:
            force = kwargs.pop('force')

        if "steamid64" not in kwargs:
            kwargs['steamid64'] = qwizi_data['steamid64']

        # Sprawdzamy czy uzytkownik o takim steamid64 juz istnieje w bazie
        if django_user_model.objects.filter(steamid64=kwargs['steamid64']).exists():
            # Sprawdzamy czy force jest ustawiony
            if force:
                # Pobieramy uzytkownika
                user = django_user_model.objects.get(steamid64=kwargs['steamid64'])
                # Usuwamy go
                user.delete()
                # Tworzymy nowego
                return django_user_model.objects.create_user_steam(**kwargs)
            else:
                # Zwracamy uzytkownika
                return django_user_model.objects.filter(steamid64=kwargs['steamid64'])[0]
        else:
            # Tworzymy uzytkownika
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
    return '<span style="color: rgba(113,118,114)">{username}</span>'


@fixture
def default_admin_role_format():
    return '<span style="color: rgba(242,0,0)">{username}</span>'


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


@fixture
def create_category(db):
    def make_category(**kwargs):
        if "name" not in kwargs:
            kwargs['name'] = 'Testowa kategoria'

            if Category.objects.filter(name=kwargs['name']).exists():
                return Category.objects.get(name=kwargs['name'])

        return Category.objects.create(**kwargs)

    return make_category


@fixture
def create_thread(db, create_category, create_user):
    def make_thread(**kwargs):
        if 'title' not in kwargs:
            kwargs['title'] = 'Testowy temat'
        if 'content' not in kwargs:
            kwargs['content'] = 'Testowa tresc'
        if 'category' not in kwargs:
            kwargs['category'] = create_category()
        if 'author' not in kwargs:
            kwargs['author'] = create_user()

        return Thread.objects.create(**kwargs)

    return make_thread


@fixture
def create_post(db, create_thread, create_user):
    def make_post(**kwargs):
        if 'thread' not in kwargs:
            kwargs['thread'] = create_thread()
        if 'content' not in kwargs:
            kwargs['content'] = 'Testowa tresc'
        if 'author' not in kwargs:
            kwargs['author'] = kwargs['thread'].author
        return Post.objects.create(**kwargs)

    return make_post


@fixture
def create_reactionitem(db):
    def make_reactionitem(**kwargs):
        return ReactionItem.objects.create(**kwargs)

    return make_reactionitem


@fixture
def create_reaction(db):
    def make_reaction(**kwargs):
        return Reaction.objects.create(**kwargs)

    return make_reaction


@fixture
def create_group(db):
    def make_group(**kwargs):
        if "tag" not in kwargs:
            kwargs['tag'] = 'vip'
        if "name" not in kwargs:
            kwargs['name'] = 'VIP'

        return Group.objects.create(**kwargs)

    return make_group


@fixture
def create_item(db, create_group):
    def make_item(**kwargs):
        if "name" not in kwargs:
            kwargs['name'] = 'VIP 7 DNI'
        if "description" not in kwargs:
            kwargs['description'] = 'VIP NA 7 DNI'
        if "price" not in kwargs:
            kwargs['price'] = Money(5, 'PLN')
        if "group" not in kwargs:
            kwargs['group'] = create_group()
        if "options" not in kwargs:
            kwargs['options'] = {
                'days': 7
            }
        return Item.objects.create(**kwargs)

    return make_item


@fixture
def create_history(db):
    def make_history(**kwargs):
        return History.objects.create(**kwargs)

    return make_history


@fixture
def create_game(db):
    def make_game(**kwargs):
        if "tag" not in kwargs:
            kwargs['tag'] = 'tf2'
        if "name" not in kwargs:
            kwargs['name'] = 'Team Fortress 2'
        if "app_id" not in kwargs:
            kwargs['app_id'] = 440

        if Game.objects.filter(tag=kwargs['tag']).exists():
            return Game.objects.get(tag=kwargs['tag'])

        return Game.objects.create(**kwargs)

    return make_game


@fixture
def create_server(db, create_game):
    def make_server(**kwargs):
        if "name" not in kwargs:
            kwargs['name'] = '(PL) JailBreak | SharkServers.pl'
        if "game" not in kwargs:
            kwargs['game'] = create_game()
        if "ip" not in kwargs:
            kwargs['ip'] = '79.133.194.18'
        if "port" not in kwargs:
            kwargs['port'] = '25004'
        return Server.objects.create(**kwargs)

    return make_server


@fixture
def create_subcategory(db):
    def make_subcategory(**kwargs):
        if "name" not in kwargs:
            kwargs['name'] = 'Subcategory'
        return SubCategory.objects.create(**kwargs)

    return make_subcategory

@fixture
def create_news(db, create_user):
    def make_news(**kwargs):
        if "title" not in kwargs:
            kwargs['title'] = 'News'
        if "content" not in kwargs:
            kwargs['content'] = 'News content'
        if "author" not in kwargs:
            kwargs['author'] = create_user()
        return News.objects.create(**kwargs)

    return make_news