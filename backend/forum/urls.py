from django.urls import path
from rest_framework import routers

from .views import (
    forum_category_list,
    forum_category_detail,
    #forum_category_create,
    ForumThreadViewSet,
    ForumPostViewSet,
    ForumCommentViewSet
)

router = routers.DefaultRouter()
router.register(r'threads', ForumThreadViewSet, basename='threads')
router.register(r'posts', ForumPostViewSet, basename='posts')
router.register(r'comments', ForumCommentViewSet, basename='comments')

urlpatterns = [
    #path('categories/', forum_category_create, name='forum-category-create'),
    path('categories/', forum_category_list, name='forum-category-list'),
    path('categories/<int:pk>/', forum_category_detail, name='forum-category-detail'),
]