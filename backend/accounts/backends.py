from django.contrib.auth.backends import BaseBackend
from django.conf import settings

from accounts.models import Account
from .steam_helpers import get_steam_user_info

import string
import random


def random_string(length):
    return ''.join(random.SystemRandom().choice(string.ascii_uppercase + string.digits) for _ in range(length))


def replace_exist_username(username):
    return '{}-{}'.format(username, random_string(5))


def create_random_username():
    return 'user{}'.format(random_string(10))


def steam_check_banned_user_names():
    pass


class SteamBackend(BaseBackend):
    def authenticate(self, request, steamid64=None):
        if steamid64:
            try:
                account = Account.objects.get(steamid64=steamid64)
            except Account.DoesNotExist:
                username = get_steam_user_info(steamid64)['username']

                username_exists = Account.objects.filter(username__iexact=username).exists()
                if username_exists:
                    username_replaced = replace_exist_username(username)
                    account = Account.objects.create_user_steam(steamid64=steamid64, username=username_replaced)
                else:
                    account = Account.objects.create_user_steam(steamid64=steamid64)
            return account

        return None

    def get_user(self, user_id):
        try:
            return Account.objects.get(pk=user_id)
        except Account.DoesNotExist:
            return None
