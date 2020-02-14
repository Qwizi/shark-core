from django.urls import path
from .views import (
    account_list,
    account_me,
    role_list,
    role_detail
)

app_name = 'accounts'

urlpatterns = [
    path('', account_list, name='accounts-list'),
    path('me/', account_me, name='accounts-me'),
    path('roles/', role_list, name='role-list'),
    path('roles/<int:pk>/', role_detail, name='role-detail')
]
