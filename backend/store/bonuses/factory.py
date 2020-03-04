from django.conf import settings

from .vip import VipBonus


class BonusFactory(object):

    @staticmethod
    def get_bonus(tag):
        if tag == 'vip':
            return VipBonus
        else:
            raise Exception(f'"{tag}" taki bonus nie istnieje')


bonus_factory = BonusFactory()
