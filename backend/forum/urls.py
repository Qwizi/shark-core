from django.urls import path, include

from .views import (
    category_list,
    category_detail,
    thread_list,
    thread_detail,
    post_list,
    post_detail,

)

app_name = 'forum'

categories_patterns = [
    path('', category_list, name='category-list'),
    path('<int:pk>/', category_detail, name='category-detail')
]

threads_patterns = [
    path('', thread_list, name='thread-list'),
    path('<int:pk>/', thread_detail, name='thread-detail')
]

posts_patterns = [
    path('', post_list, name='post-list'),
    path('<int:pk>/', post_detail, name='post-detail')
]

urlpatterns = [
    path('categories/', include(categories_patterns)),
    path('threads/', include(threads_patterns)),
    path('posts/', include(posts_patterns))
]

"""
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
"""
