from django.urls import path, re_path
from .views import AccountSingUpView, AccountActivateView

app_name = 'accounts'

urlpatterns = [
    path('sign-up/', AccountSingUpView.as_view(), name='sign-up'),
    re_path(r'^activate/'
            r'(?P<aidb64>[0-9A-Za-z_\-]+)/'
            r'(?P<token>[0-9A-Za-z]{1,13}'
            r'-[0-9A-Za-z]{1,20})/$',
            AccountActivateView.as_view(), name='activate'),
]
