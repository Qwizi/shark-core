from rest_framework import routers
from .views import CategoryViewSet, BonusViewSet

router = routers.DefaultRouter()
router.register(r'categories', CategoryViewSet)
router.register(r'bonuses', BonusViewSet, basename='bonuses')

app_name = 'store'

urlpatterns = router.urls