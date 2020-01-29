from django.urls import path, include

from accounts.views import AccountAuthSteamTokenView

app_name = 'api'

urlpatterns = [
    path('auth/token/', AccountAuthSteamTokenView.as_view()),
    path('accounts/', include('accounts.urls')),
    path('store/', include('store.urls')),
    path('forum/', include('forum.urls')),
    path('sourcemod/', include('smadmins.urls')),
    path('sourcemod/', include('servers.urls'))
]