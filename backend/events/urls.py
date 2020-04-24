from django.urls import path

from .views import event_list, event_detail

app_name = 'events'

urlpatterns = [
    path('', event_list, name='list'),
    path('<int:pk>/', event_detail, name='detail')
]
