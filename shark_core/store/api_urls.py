from django.urls import path, include
from rest_framework import routers
from .api_views import CategoryViewSet, BonusViewSet

router = routers.DefaultRouter()
router.register(r'categories', CategoryViewSet)
router.register(r'bonuses', BonusViewSet, basename='bonuses')

app_name = 'store'

urlpatterns = router.urls