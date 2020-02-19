from django.urls import path, include

from accounts.views import AccountAuthSteamTokenView, ServerAccountAuthSteamTokenView

app_name = 'api'

urlpatterns = [
    path('oauth/',  include('oauth2_provider.urls', namespace='oauth2_provider')),
    path('auth/token/', AccountAuthSteamTokenView.as_view()),
    path('auth/server/token/', ServerAccountAuthSteamTokenView.as_view()),
    path('accounts/', include('accounts.urls', namespace='accounts')),
    path('store/', include('store.urls')),
    path('forum/', include('forum.urls')),
    path('sourcemod/', include('smadmins.urls')),
    path('sourcemod/', include('servers.urls')),
    path('steambot/', include('steambot.urls', namespace='steambot'))
]