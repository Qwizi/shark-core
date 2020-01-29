from django.test import TestCase
from ..models import Account

class AccountModelTestCase(TestCase):

    def setUp(self):
        Account.objects.create(
            ""
        )
