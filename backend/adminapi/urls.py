from django.urls import path, include

app_name = 'adminapi'

urlpatterns = [
    path('accounts/', include('accounts.urls_admin', namespace='accounts'))
]
