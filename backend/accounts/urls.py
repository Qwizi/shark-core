from django.urls import path, include
from rest_framework import routers

from .views import AccountView, AccountAuthSteamTokenView

router = routers.DefaultRouter()
router.register(r'', AccountView, basename='accounts')

app_name = 'accounts'

urlpatterns = [
    path('', include(router.urls)),
]
