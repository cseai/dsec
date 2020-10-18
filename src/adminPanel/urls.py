from django.urls import path
from .views import (index,all_store_request,store_details)
app_name='adminpanel'
urlpatterns = [
    path('',index,name='home'),
    path('store-request/',all_store_request,name='store_request'),
    path('store-details/<int:store_id>',store_details,name='store_details'),
]
