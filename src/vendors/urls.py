from django.urls import path

from .views import (
        vendor_home_view,
        register_store_view,
        store_detail_view,
        store_update_view,
        store_product_list_view,
        store_product_add_view,
        store_product_detail_view,
        store_product_update_view,
        store_product_remove_view,
        api_store_product_detail_view,
    )

app_name = 'vendors'
urlpatterns = [
    path('', vendor_home_view, name='home'),
    path('register/', register_store_view, name='register_store'),
    path('stores/<str:store_username>/', store_detail_view, name='store_detail'),
    path('stores/<str:store_username>/update/', store_update_view, name='store_update'),
    path('stores/<str:store_username>/products/', store_product_list_view, name='store_product_list'),
    path('stores/<str:store_username>/products/add/', store_product_add_view, name='store_product_add'),
    path('stores/<str:store_username>/products/<int:product_id>/', store_product_detail_view, name='store_product_detail'),
    path('stores/<str:store_username>/products/<int:product_id>/update/', store_product_update_view, name='store_product_update'),
    path('stores/<str:store_username>/products/<int:product_id>/remove/', store_product_remove_view, name='store_product_remove'),
    #api
    path('api/stores/store_username/products/product_id/', api_store_product_detail_view, name='api_store_product_detail'),

]