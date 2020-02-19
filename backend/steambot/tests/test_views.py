import pytest
from django.urls import reverse

from accounts.tests.fixtures import *

from ..views import (
    SteamBotQueueListCreateView
)


@pytest.mark.django_db
def test_queue_list_view(
        api_factory
):
    view = SteamBotQueueListCreateView.as_view()
    request = api_factory.get(reverse('api:steambot:queue'))
    response = view(request)

    assert response.status_code == 200


@pytest.mark.django_db
def test_queue_create_view_without_authenticate(
        api_factory
):
    view = SteamBotQueueListCreateView.as_view()
    request = api_factory.post(reverse('api:steambot:queue'))
    response = view(request)

    assert response.status_code == 401


@pytest.mark.django_db
def test_queue_create_view_with_authenticate(
        api_factory, create_user, get_token_for_user
):
    user = create_user()
    view = SteamBotQueueListCreateView.as_view()
    request = api_factory.post(reverse('api:steambot:queue'))
    force_authenticate(request, user=user, token=get_token_for_user(user=user))
    response = view(request)

    assert response.status_code == 201


@pytest.mark.django_db
@pytest.mark.parametrize(
    'queue_count, status_code', [
        pytest.param(
            1, 200
        ),
        pytest.param(
            0, 200
        )
    ]
)
def test_queue_list_renders(
        queue_count, status_code, api_client, create_queue, create_user
):
    if queue_count == 1:
        user = create_user()
        create_queue(account=user)

    response = api_client.get(reverse('api:steambot:queue'))

    assert response.status_code == status_code
    assert response.data['count'] == queue_count


@pytest.mark.django_db
def test_queue_create_renders_without_authenticate(
        api_client
):
    response = api_client.post(reverse('api:steambot:queue'))

    assert response.status_code == 401


@pytest.mark.django_db
def test_queue_create_renders_with_authenticate(
        api_client_with_credentials, qwizi_data
):
    response = api_client_with_credentials.post(reverse('api:steambot:queue'))

    second_response = api_client_with_credentials.get(reverse('api:steambot:queue'))

    assert response.status_code == 201
    assert second_response.data['count'] == 1
    assert second_response.data['results'][0]['account']['tradeurl'] == qwizi_data['tradeurl']
    assert second_response.data['results'][0]['account']['steamid64'] == qwizi_data['steamid64']
