from django.urls import path

from .views import (
    forum_category_list,
    forum_category_detail,
    forum_thread_list,
    forum_thread_create,
    forum_thread_detail,
    forum_post_list,
    forum_post_create,
    forum_post_detail,
)

urlpatterns = [
    path('categories/', forum_category_list, name='forum-category-list'),
    path('categories/<int:pk>/', forum_category_detail, name='forum-category-detail'),
    path('threads/', forum_thread_list, name='forum-thread-list'),
    path('threads/create', forum_thread_create, name='forum-thread-create'),
    path('threads/<int:pk>/', forum_thread_detail, name='forum-thread-detail'),
    path('posts/', forum_post_list, name='forum-post-list'),
    path('posts/<int:pk>/', forum_post_detail, name='forum-post-detail'),
    path('posts/create', forum_post_create, name='forum-post-create')
]
