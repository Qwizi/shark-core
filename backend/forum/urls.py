from django.urls import path, include

from .views import (
    category_list,
    category_detail,
    thread_list,
    thread_detail,
    thread_reactions_list,
    thread_set_best_answer,
    thread_unset_best_answer,
    post_list,
    post_detail,
    stats_list,
    reaction_list
)

app_name = 'forum'

categories_patterns = [
    path('', category_list, name='category-list'),
    path('<int:pk>/', category_detail, name='category-detail')
]

threads_patterns = [
    path('', thread_list, name='thread-list'),
    path('<int:pk>/', thread_detail, name='thread-detail'),
    path('<int:thread_pk>/reactions/', thread_reactions_list, name='thread-reactions-list'),
    path('<int:pk>/best-answer/set/', thread_set_best_answer, name='thread-set-best-answer'),
    path('<int:pk>/best-answer/unset/', thread_unset_best_answer, name='thread-unset-best-answer')
]

posts_patterns = [
    path('', post_list, name='post-list'),
    path('<int:pk>/', post_detail, name='post-detail')
]

urlpatterns = [
    path('categories/', include(categories_patterns)),
    path('threads/', include(threads_patterns)),
    path('posts/', include(posts_patterns)),
    path('stats/', stats_list, name='stats-list'),
    path('reactions/', reaction_list, name='reactions-list')
]
