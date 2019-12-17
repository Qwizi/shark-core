from .bonus import BaseBonus


class PremiumAccountBonus(BaseBonus):
    TAG = 'premium_account'

    def add_bonus(self, *args, **kwargs):
        options = self.model_instance.get_options()

        account_id = kwargs['account_id']
        premium_group_id = options['group_id']

        account = self.get_group_by_id(account_id)
        group = self.get_group_by_id(premium_group_id)

        group.user_set.add(account)

        return 'Done.'
