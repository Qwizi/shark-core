from django.urls import path

from .views import PremiumAccountCronView

urlpatterns = [
    path('', PremiumAccountCronView.as_view())
]