from django.urls import path, include
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

role_patterns = [
    path('', role_list, name='role-list'),
    path('<int:pk>/', role_detail, name='role-detail', )
]

wallet_patterns = [
    path('', account_me_wallet_list, name='me-wallet-list'),
    path('<int:wtype>/exchange', account_me_wallet_exchange, name='me-wallet-exchange')
]

me_patterns = [
    path('', account_me, name='me-detail'),
    path('display-role/', account_me_update_display_role, name='me-update-display-role'),
    path('wallets/', include(wallet_patterns))
]

urlpatterns = [
    path('', account_list, name='list'),
    path('me/', include(me_patterns)),
    path('roles/', include(role_patterns))
]

"""

urlpatterns = [
    path('', account_list, name='list'),
    path('me/', account_me, name='me'),
    path('me/display-role/', account_me_update_display_role, name='me-update-display-role'),
    path('me/wallets/', account_me_wallet_list, name='me-wallet-list'),
    path('me/wallets/<int:wtype>/', account_me_wallet_exchange, name='me-wallet-exchange'),
    path('roles/', role_list, name='role-list'),
    path('roles/<int:pk>/', role_detail, name='role-detail')
]
"""
