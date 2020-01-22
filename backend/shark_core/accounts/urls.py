from django.urls import path, re_path
from rest_framework import routers

from .views import AccountViewSet

router = routers.DefaultRouter()
router.register(r'', AccountViewSet, basename='accounts')

app_name = 'accounts'

urlpatterns = router.urls
