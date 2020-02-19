import pytest
from .fixtures import *


@pytest.mark.django_db
def test_payment_manager_bonuscodes_get_provider_class_with_valid_code(create_bonuscode):
    bonus_code = create_bonuscode(
        code="TEST",
        money=Money(2, 'PLN')
    )

    provider_class = payment_manager.bonuscodes.get_provider_class()
    provider_instance = provider_class(code=bonus_code.code)

    assert provider_instance.is_valid() is True


@pytest.mark.django_db
def test_payment_manager_bonuscodes_get_provider_class_without_valid_code():
    bonus_code = "TEST"

    provider_class = payment_manager.bonuscodes.get_provider_class()
    provider_instance = provider_class(code=bonus_code)

    assert provider_instance.is_valid() is False
