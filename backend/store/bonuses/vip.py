from .base import BonusBase
from servers.models import Server
from ..models import Item, VipCache

import datetime

class VipBonus(BonusBase):

    def __init__(self, item_obj: Item, **kwargs):
        super(VipBonus, self).__init__(item_obj, **kwargs)

        self.create_field(name='server', type='select', choices=self.get_server_choices())

    @staticmethod
    def get_server_choices():
        servers = Server.objects.all()
        choices = []

        for server in servers:
            server_detail = {
                'id': server.id,
                'name': server.name,
            }
            choices.append(server_detail)

        return choices

    def after_bought(self, **kwargs):
        user = kwargs.get('user', None)
        extra_fields = kwargs.get('extra_fields', None)
        server = extra_fields.get('server', None)
        server_instance = Server.objects.get(pk=server)
        flag = self.get_option('flag')
        days = self.get_option('days')

        days_to_add = datetime.timedelta(days=days)

        return VipCache.objects.create(
            user=user,
            flag=flag,
            server=server_instance,
            end=days_to_add
        )

