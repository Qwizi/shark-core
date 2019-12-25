from django.urls import path, include
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView
)
app_name = 'api'

urlpatterns = [
    path('auth/token/', TokenObtainPairView.as_view(), name='token_optain_pair'),
    path('auth/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('store/', include('store.api_urls'))
]