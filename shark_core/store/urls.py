from django.urls import path, include
from rest_framework import routers
from .views import StoreCategoryViewSet, StoreBonusViewSet, StoreCheckoutView

router = routers.DefaultRouter()
router.register(r'categories', StoreCategoryViewSet)
router.register(r'bonuses', StoreBonusViewSet, basename='bonuses')

app_name = 'store'

urlpatterns = [
    path('', include(router.urls)),
    path('checkout/', StoreCheckoutView.as_view())
]