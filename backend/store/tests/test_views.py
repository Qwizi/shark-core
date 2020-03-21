import pytest
from django.shortcuts import reverse

from accounts.tests.fixtures import *

from ..views import (
    ItemListView,
    OfferCreateView
)


@pytest.mark.django_db
def test_store_item_list_view(
        api_factory
):
    view = ItemListView.as_view()
    request = api_factory.get(reverse('api:store:item-list'))
    response = view(request)

    assert response.status_code == 200


@pytest.mark.django_db
def test_store_offer_create_without_authenticate_view(
        api_factory
):
    view = OfferCreateView.as_view()
    request = api_factory.post(reverse('api:store:offer-create'))
    response = view(request)

    assert response.status_code == 401


@pytest.mark.django_db
def test_store_offer_create_view(
        api_factory, create_user, get_token_for_user, create_group, create_item
):
    user = create_user()
    wallet = user.wallet_set.get(wtype=Wallet.WalletTypeChoices.PRIMARY)
    wallet.add_money(Money(5, 'PLN'))

    group = create_group(
        tag='vip',
        name='VIP'
    )
    item = create_item(
        name='VIP 7 DNI',
        description='VIP NA 7 DNI',
        price=Money('5', 'PLN'),
        options={
            'days': 7,
            'flag': 'a'
        },
        group=group
    )

    data = {
        'item': item.id,
        'wallet_type': Wallet.WalletTypeChoices.PRIMARY.value,
    }

    view = OfferCreateView.as_view()
    request = api_factory.post(reverse('api:store:offer-create'), data=data)
    force_authenticate(request, user=user, token=get_token_for_user(user=user))
    response = view(request)

    assert response.status_code == 201


@pytest.mark.django_db
def test_store_item_list_renders(
        api_client, create_user, create_item, create_group
):
    user = create_user()
    group = create_group(
        tag='vip',
        name='VIP'
    )
    item = create_item(
        name='VIP 7 DNI',
        description='VIP NA 7 DNI',
        price=Money(5, 'PLN'),
        options={
            'days': 7,
            'flag': 'a'
        },
        group=group
    )

    response = api_client.get(reverse('api:store:item-list'))

    assert response.status_code == 200
    assert response.data['count'] == 1
    assert response.data['results'][0]['options']['days'] == 7
    assert response.data['results'][0]['options']['flag'] == "a"
    assert "fields" in response.data['results'][0]


@pytest.mark.django_db
def test_store_offer_create_renders(
        api_client_with_credentials, create_item, create_server, create_user
):
    user = create_user()

    wallet = user.wallet_set.get(wtype=Wallet.WalletTypeChoices.PRIMARY)
    wallet.add_money(Money(90000, 'PLN'))

    item = create_item(options={
        'days': 7,
        'flag': 'a'
    })
    server = create_server()
    extra_fields = [{'server': server.pk}]

    data = {
        'item': item.id,
        'extra_fields': extra_fields,
        'wallet_type': Wallet.WalletTypeChoices.PRIMARY
    }

    response = api_client_with_credentials.post(reverse('api:store:offer-create'), data=data)

    assert response.status_code == 201
    assert History.objects.filter(user=user).count() == 1
    assert VipCache.objects.filter(user=user).count() == 1
    assert VipCache.objects.get(user=user).server == server
    assert VipCache.objects.get(user=user).flag == 'a'
