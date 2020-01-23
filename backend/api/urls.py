from django.urls import path, include
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
app_name = 'api'

urlpatterns = [
    path('token/auth/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('accounts/', include('accounts.urls')),
    path('store/', include('store.urls')),
    path('forum/', include('forum.urls')),
    path('sourcemod/', include('smadmins.urls')),
    path('sourcemod/', include('servers.urls'))
]