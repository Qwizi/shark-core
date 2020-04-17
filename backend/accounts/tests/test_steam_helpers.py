import pytest
from .fixtures import *


@pytest.mark.django_db
def test_get_steam_user_info_with_valid_steamid64(qwizi_data):
    user_data = get_steam_user_info(steamid64=qwizi_data['steamid64'])
    user_data.pop('avatar')
    user_data.pop('profileurl')
    user_data.pop('avatarmedium')
    user_data.pop('avatarfull')
    assert user_data == qwizi_data


@pytest.mark.django_db
def test_get_steam_user_info_without_valid_steamid64():
    steamid64 = "INVALID"

    with pytest.raises(Exception) as context:
        get_steam_user_info(steamid64=steamid64)
    assert "Invalid steamid64" in str(context.value)
