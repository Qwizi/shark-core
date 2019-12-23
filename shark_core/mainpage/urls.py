from django.urls import path
from .views import MainPageIndex

app_name = 'mainpage'

urlpatterns = [
    path('', MainPageIndex.as_view(), name='index')
]