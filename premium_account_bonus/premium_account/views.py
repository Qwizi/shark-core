from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import PremiumCache as pc
import datetime


class PremiumAccountCronView(APIView):

    def get(self, request):
        for premium in pc.objects.filter(time__lte=datetime.datetime.now()):
            premium.account.display_group = premium.old_group
            premium.account.save()
            premium.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        return Response(status=status.HTTP_204_NO_CONTENT)
