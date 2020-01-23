from django.urls import path, include
from rest_framework import routers
from .views import StoreCategoryViewSet, StoreBonusViewSet, StoreOfferView

router = routers.SimpleRouter()
router.register(r'categories', StoreCategoryViewSet)
router.register(r'bonuses', StoreBonusViewSet, basename='bonuses')
app_name = 'store'

cron_urlpatterns = [
    path('premium-account-cache/', include('premium_account.urls'))
]

urlpatterns = [
    path('', include(router.urls)),
    path('cron/', include(cron_urlpatterns)),
    path('offer/', StoreOfferView.as_view()),
]