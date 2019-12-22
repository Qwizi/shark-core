from django.urls import path

from .views import (
    StoreBonusesView,
    StoreBonusDetailView,
)

app_name = 'store'

urlpatterns = [
    path('', StoreBonusesView.as_view(), name='index'),
    path('bonus-<int:bonus_id>/', StoreBonusDetailView.as_view(), name='detail'),
]