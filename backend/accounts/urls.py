from django.urls import path, include
from rest_framework import routers

from .views import (
    account_list,
    account_me,
    AccountView,
)

router = routers.DefaultRouter()
router.register(r'', AccountView, basename='accounts')

app_name = 'accounts'

urlpatterns = [
    path('', account_list, name='accounts-list'),
    path('me/', account_me, name='accounts-me')
    #path('', include(router.urls)),
]
