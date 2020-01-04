from store.base_bonus import BaseBonus
from accounts.models import Group

from .models import PremiumCache as pc
import datetime


class PremiumAccountBonus(BaseBonus):
    TAG = 'premium_account'

    def execute(self, *args, **kwargs):
        new_group, created = Group.objects.get_or_create(pk=self.options['group'], name="Premium")

        if pc.objects.filter(account=self.account).exists():
            premium_cache = pc.objects.filter(account=self.account).first()
            premium_cache.time += datetime.timedelta(days=self.options['days'])
            premium_cache.save()
        else:
            end_date = datetime.datetime.now() + datetime.timedelta(days=self.options['days'])

            premium_cache = pc()
            premium_cache.account = self.account
            premium_cache.old_group = self.account.display_group
            premium_cache.new_group = new_group
            premium_cache.time = end_date
            premium_cache.save()

            self.account.display_group = new_group
            self.account.save()

            self.account.groups.add(new_group)

            print(new_group)
            print(self.account.display_group)
            print(self.account.groups.all())
            print(premium_cache)
