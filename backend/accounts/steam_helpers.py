from django.conf import settings
from steam.webapi import WebAPI
from steam.steamid import SteamID
from shark_core.helpers import get_shark_core_setting

def check_steam_settings_exist():
    steam_settings = get_shark_core_setting("STEAM")



def get_steam_api_key():
    try:
        api_key = settings.SHARK_CORE['STEAM']['API_KEY']
    except KeyError:
        raise Exception('Steam api key not set')

    return api_key


def get_steam_user_info(steamid64, username=None):
    s_api = WebAPI(get_steam_api_key())

    results = s_api.call('ISteamUser.GetPlayerSummaries', steamids=steamid64)

    if len(results['response']['players']) == 0:
        raise Exception('Invalid steamid64')

    player = results['response']['players'][0]

    if username is None:
        username = player['personaname']

    profileurl = player['profileurl']
    avatar = player['avatar']
    avatarmedium = player['avatarmedium']
    avatarfull = player['avatarfull']
    loccountrycode = player.get('loccountrycode', None)

    steamid64_from_player = player['steamid']
    steamid32 = SteamID(steamid64_from_player).as_steam2
    steamid3 = SteamID(steamid64_from_player).as_steam3

    return {
        'username': username,
        'steamid64': steamid64_from_player,
        'steamid32': steamid32,
        'steamid3': steamid3,
        'profileurl': profileurl,
        'avatar': avatar,
        'avatarmedium': avatarmedium,
        'avatarfull': avatarfull,
        'loccountrycode': loccountrycode

    }
