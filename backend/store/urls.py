from django.urls import path, include

from .views import (
    item_list,
    offer_create
)

app_name = 'store'

offer_patterns = [
    path('', offer_create, name='offer-create')
]

item_patterns = [
    path('', item_list, name='item-list')
]

urlpatterns = [
    path('items/', include(item_patterns)),
    path('offer/', include(offer_patterns))
]
