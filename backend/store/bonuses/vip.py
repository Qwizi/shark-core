from .base import BonusBase
from ..forms import VipForm


class VipBonus(BonusBase):
    form = VipForm
    
    def after_bought(self, **kwargs):
        pass
