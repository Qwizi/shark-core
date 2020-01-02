from django.urls import path, include
app_name = 'api'

urlpatterns = [
    path('auth/', include('djoser.urls')),
    path('auth/', include('djoser.urls.authtoken')),
    path('users/', include('accounts.urls')),
    path('store/', include('store.urls')),
    path('servers/', include('servers.urls'))
]