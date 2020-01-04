from django.urls import path, include
from rest_framework_jwt.views import obtain_jwt_token, refresh_jwt_token
app_name = 'api'

urlpatterns = [
    path('token/auth/', obtain_jwt_token),
    path('token/refresh/', refresh_jwt_token),
    path('accounts/', include('accounts.urls')),
    path('store/', include('store.urls')),
    path('servers/', include('servers.urls'))
]