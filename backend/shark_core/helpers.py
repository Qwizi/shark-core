from django.conf import settings

import random
import string
import re


def get_shark_core_settings(setting_name: str):
    try:
        shark_core_setting = getattr(settings, "SHARK_CORE")
    except AttributeError:
        raise Exception('Setting SHARK_CORE is not exists')

    setting = shark_core_setting.get(setting_name, None)

    if setting is None:
        raise Exception('Setting {} not exist in SHARK_CORE', format(setting_name))

    return setting


def get_steam_setting(setting_name: str):
    steam_settings = get_shark_core_settings("STEAM")

    setting = steam_settings.get(setting_name, None)

    if setting is None:
        raise Exception('Setting {} not exist in STEAM'.format(setting_name))

    return setting


def random_string(length: int) -> str:
    """
    Funkcja zwracajaca losowy string
    :param length:
    :return:
    """
    return ''.join(random.SystemRandom().choice(string.ascii_uppercase + string.digits) for _ in range(length))


def create_random_username() -> str:
    """
    Funcja zwracająca losowa nazwe uzytkownika
    :return:
    """
    return 'user-{}'.format(random_string(10))


def check_banned_usernames(username: str, source=None) -> str:
    """
    Funkcja sprawdzajaca czy podana nazwa uzytkownika jest w ustawieniach nazw zbanowanycych
    """
    check_banned_user_names = get_steam_setting('CHECK_BANNED_USER_NAMES')
    if check_banned_user_names:
        if source:
            banned_usernames = source
        else:
            banned_usernames = get_steam_setting('BANNED_USER_NAMES')

        for b_username in banned_usernames:
            r = re.match(r'{}'.format(b_username), username)

            if r:
                username = create_random_username()
    return username
