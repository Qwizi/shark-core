from django.urls import path, include

app_name = 'api'

urlpatterns = [
    path('store/', include('store.api_urls'))
]