from django.urls import path, include
from accounts.views import steam_token_obtain_pair
from rest_framework_simplejwt.views import (
    token_refresh,
    #token_obtain_pair
)
app_name = 'api'

urlpatterns = [
    path('token/auth/', steam_token_obtain_pair, name='token_obtain_pair'),
    path('token/refresh/', token_refresh, name='token_refresh'),
    path('accounts/', include('accounts.urls')),
    path('store/', include('store.urls')),
    path('forum/', include('forum.urls')),
    path('sourcemod/', include('smadmins.urls')),
    path('sourcemod/', include('servers.urls'))
]