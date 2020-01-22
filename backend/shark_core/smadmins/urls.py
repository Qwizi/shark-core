from rest_framework import routers

from .views import AdminViewSet

router = routers.DefaultRouter()
router.register(r'admins', AdminViewSet, basename='sm-admins')

urlpatterns = router.urls