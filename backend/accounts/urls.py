from django.urls import path
from .views import (
    account_list,
    account_me,
    account_me_update_display_role,
    account_me_wallet_list,
    account_me_wallet_exchange,
    role_list,
    role_detail
)

app_name = 'accounts'

urlpatterns = [
    path('', account_list, name='accounts-list'),
    path('me/', account_me, name='accounts-me'),
    path('me/display-role/', account_me_update_display_role, name='accounts-me-update-display-role'),
    path('me/wallets/', account_me_wallet_list, name='accounts-me-wallet-list'),
    path('me/wallets/<int:wtype>/', account_me_wallet_exchange, name='accounts-me-wallet-exchange'),
    path('roles/', role_list, name='role-list'),
    path('roles/<int:pk>/', role_detail, name='role-detail')
]
