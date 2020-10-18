from django.urls import path

from .views import (register_vendor_store_view,index)

app_name = 'vendors'
urlpatterns = [
    path('register/', register_vendor_store_view, name='register-store'),
    path('', index, name='home'),
]