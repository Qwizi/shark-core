from django.urls import path, include
from django.conf.urls import url

from rest_framework import routers

from .views import (
    AdminAccountViewSet,
    admin_account
)

router = routers.SimpleRouter()
router.register(r'', AdminAccountViewSet, basename='accounts')

app_name = 'accounts'

urlpatterns = [
    path('', AdminAccountViewSet.as_view({'get': 'list', 'post': 'create'}), name='list'),
    path('<int:pk>/', AdminAccountViewSet.as_view({'get': 'retrieve', 'put': 'update', 'delete': 'destroy'}),
         name='detail')
]
