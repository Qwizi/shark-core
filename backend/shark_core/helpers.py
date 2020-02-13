from django.conf import settings

import random
import string
import re


def get_shark_core_settings(setting_name: str):
    """
    Funkcja pobierajaca ustawienie z SHARK_CORE
    """

    # Sprawdzamy czy w ustawieniach znajduje sie SHARK_CORE
    # Jezeli nie wywietlamy wyjatek
    try:
        shark_core_setting = getattr(settings, "SHARK_CORE")
    except AttributeError:
        raise Exception('Setting SHARK_CORE is not exists')

    # Pobieramy ustawienie
    setting = shark_core_setting.get(setting_name, None)

    # Jezeli nazwa ustwawienia jest niepoprawna wyswietlamy wyjatek
    if setting is None:
        raise Exception('Setting {} not exist in SHARK_CORE', format(setting_name))

    return setting


def get_steam_setting(setting_name: str):
    """
    Funkcja pobierajaca ustawienia od STEAMA
    """

    # Pobieranie slownika z ustawieniami STEAMA
    steam_settings = get_shark_core_settings("STEAM")

    # Pobieranie ustawien steama
    setting = steam_settings.get(setting_name, None)

    # Jezli nazwa ustawnien steama jest nieporawna zwracamy wyjatek
    if setting is None:
        raise Exception('Setting {} not exist in STEAM'.format(setting_name))

    return setting


def random_string(length: int) -> str:
    """
    Funkcja zwracajaca losowy string
    """
    return ''.join(random.SystemRandom().choice(string.ascii_uppercase + string.digits) for _ in range(length))


def create_random_username() -> str:
    """
    Funcja zwracająca losowa nazwe uzytkownika
    """
    return 'user-{}'.format(random_string(10))


def check_banned_usernames(username: str, source: list = None) -> str:
    """
    Funkcja sprawdzajaca czy podana nazwa uzytkownika jest w ustawieniach nazw zbanowanycych
    """

    # Sprawdzamy czy jest wlaczone ustawienie od sprawdzania zbanowanych nazw uzytkowkna
    check_banned_user_names = get_steam_setting('CHECK_BANNED_USER_NAMES')

    # Jezeli tak przeprowadzamy sprawdzanie nazwy uzytkownika
    if check_banned_user_names:
        # Jezeli argument source jest ustawiony uzupelniany zmienna odpowiedna wartoscią
        if source:
            banned_usernames = source
        else:
            # Jezeli nie pobieramy liste zbanowanych nazw uzytkownika z ustawien
            banned_usernames = get_steam_setting('BANNED_USER_NAMES')

        # Petla iterujaca po liscie zbanowanych nazw
        for b_username in banned_usernames:
            r = re.match(r'{}'.format(b_username), username)

            if r:
                username = create_random_username()
    return username
