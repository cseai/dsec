from django.urls import path

from .views import (
        store_list_view,
        store_detail_view,
        store_product_list_view,
        store_product_detail_view,
    )

app_name = 'stores'
urlpatterns = [
    path('', store_list_view, name='stores'),
    path('<str:store_username>/', store_detail_view, name='store_detail'),
    path('<str:store_username>/products/', store_product_list_view, name='store_product_list'),
    path('<str:store_username>/products/<int:product_id>/', store_product_detail_view, name='store_product_detail'),
]