from django.urls import path

from .views import news_list, news_detail

app_name = 'news'

urlpatterns = [
    path('', news_list, name='list'),
    path('<int:pk>/', news_detail, name='detail')
]
