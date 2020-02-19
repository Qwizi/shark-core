from django.urls import path

from .views import (
    steambot_queue
)

app_name = 'steambot'

urlpatterns = [
    path('queue/', steambot_queue, name='queue')
]
