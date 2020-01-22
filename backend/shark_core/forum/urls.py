from rest_framework import routers

from .views import (
    ForumCategoryViewSet,
    ForumThreadViewSet,
    ForumPostViewSet,
    ForumCommentViewSet
)

router = routers.DefaultRouter()
router.register(r'categories', ForumCategoryViewSet)
router.register(r'threads', ForumThreadViewSet, basename='threads')
router.register(r'posts', ForumPostViewSet, basename='posts')
router.register(r'comments', ForumCommentViewSet, basename='comments')

urlpatterns = router.urls