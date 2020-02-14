from django.test import TestCase

from djmoney.money import Money

from ..providers import payment_manager

from ..models import (
    BonusCode
)


class AccountProvidersTestCase(TestCase):

    def setUp(self):
        self.code = "TEST"
        self.bonus_code = BonusCode.objects.create(
            code=self.code,
            money=Money(2, 'PLN')
        )

    def test_payment_manager_bonuscodes_get_provider_class_valid_code(self):
        ProviderClass = payment_manager.bonuscodes.get_provider_class()
        provider = ProviderClass(model=BonusCode, code=self.code)
        self.assertTrue(provider)

        provider_validate = provider.validate()

        self.assertTrue(provider_validate)

        if provider.validate():
            money = provider.get_money()
            self.assertEqual(money, Money(2, 'PLN'))

    def test_payment_manager_bonuscodes_get_provider_class_invalid_code(self):
        ProviderClass = payment_manager.bonuscodes.get_provider_class()
        invalid_code = "INVALID"
        provider = ProviderClass(model=BonusCode, code=invalid_code)

        provider_validate = provider.validate()

        self.assertFalse(provider_validate)

    def test_payment_manager_sms_get_provider_class(self):
        self.assertTrue(payment_manager.sms.get_provider_class())

    def test_payment_manager_transfer_get_provider_class(self):
        self.assertTrue(payment_manager.transfer.get_provider_class())
