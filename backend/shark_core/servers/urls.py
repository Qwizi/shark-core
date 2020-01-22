from rest_framework import routers
from django.urls import path, include

from .views import ServerViewSet, ServerStatusViewSet

router = routers.DefaultRouter()
router.register('', ServerViewSet, basename='servers')
# router.register('status/', ServerStatusViewSet, basename='servers-status')

urlpatterns = [
    path('', include(router.urls)),
]