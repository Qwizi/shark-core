from django.urls import path, include

from .views import (
    category_list,
    category_detail,
    thread_list,
    thread_detail,
    post_list,
    post_detail,
    thread_reaction_add
)

app_name = 'forum'

categories_patterns = [
    path('', category_list, name='category-list'),
    path('<int:pk>/', category_detail, name='category-detail')
]

thread_reactions_patterns = [
    path('add/', thread_reaction_add, name='thread-reaction-add')
]

threads_patterns = [
    path('', thread_list, name='thread-list'),
    path('<int:pk>/', thread_detail, name='thread-detail'),
    path('<int:thread_pk>/reactions/', include(thread_reactions_patterns))
]

posts_patterns = [
    path('', post_list, name='post-list'),
    path('<int:pk>/', post_detail, name='post-detail')
]

urlpatterns = [
    path('categories/', include(categories_patterns)),
    path('threads/', include(threads_patterns)),
    path('posts/', include(posts_patterns)),
]
