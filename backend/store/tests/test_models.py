import pytest

from accounts.tests.fixtures import *


@pytest.mark.django_db
def test_store_group_create(
        create_group
):
    group = create_group(
        name='Vip'
    )

    assert group.name == 'Vip'


@pytest.mark.django_db
def test_store_item_create(
        create_group, create_item
):
    group = create_group(
        tag='vip',
        name='Vip'
    )

    item = create_item(
        name='VIP 7 DNI',
        description='VIP na 7 dni',
        options={
            'days': 7
        },
        price=Money(5, 'PLN'),
        group=group
    )

    assert item.name == 'VIP 7 DNI'
    assert item.description == 'VIP na 7 dni'
    assert Item.objects.filter(options__days=7)[0] == item
    assert item.group == group


@pytest.mark.django_db
def test_store_history_create(
        create_user, create_group, create_item, create_history
):
    user = create_user()
    group = create_group(
        tag='vip',
        name='Vip'
    )
    item = create_item(
        name='VIP 7 DNI',
        description='VIP na 7 dni',
        options={
            'days': 7
        },
        price=Money(5, 'PLN'),
        group=group
    )
    history = create_history(
        user=user,
        item=item
    )

    assert history.user == user
    assert history.item == item
