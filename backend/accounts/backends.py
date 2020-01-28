from django.contrib.auth.backends import BaseBackend

from accounts.models import Account
from .steam_helper import get_steam_user_info

class SteamBackend(BaseBackend):
    def authenticate(self, request, steamid64=None):
        if steamid64:
            try:
                account = Account.objects.get(steamid64=steamid64)
            except Account.DoesNotExist:
                user_info = get_steam_user_info(steamid64=steamid64)

                account = Account()
                account.username = user_info['username']
                account.steamid64 = user_info['steamid64']
                account.steamid32 = user_info['steamid32']
                account.steamid3 = user_info['steamid3']
                account.save()
            return account

        return None

    def get_user(self, user_id):
        try:
            return Account.objects.get(pk=user_id)
        except Account.DoesNotExist:
            return None
