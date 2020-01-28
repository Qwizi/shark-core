from django.conf import settings
from steam.webapi import WebAPI
from steam.steamid import SteamID

API_KEY = settings.SHARK_CORE['STEAM']['API_KEY']


def get_steam_user_info(steamid64):
    s_api = WebAPI(API_KEY)
    results = s_api.ISteamUser.GetPlayerSummaries(steamids=steamid64)
    player = results['response']['players'][0]

    username = player['personaname']

    steamid64_from_player = player['steamid']
    steamid32 = SteamID(steamid64_from_player).as_steam2
    steamid3 = SteamID(steamid64_from_player).as_steam3

    return {
        'username': username,
        'steamid64': steamid64_from_player,
        'steamid32': steamid32,
        'steamid3': steamid3
    }
