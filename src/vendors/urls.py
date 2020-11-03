from django.urls import path

from .views import (register_vendor_store_view,index,product_details)

app_name = 'vendors'
urlpatterns = [
    path('register/', register_vendor_store_view, name='register_store'),
    path('product-details/', product_details, name='product_details'),
    path('', index, name='home'),
]