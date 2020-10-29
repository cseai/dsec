from django.urls import path,include
from .views import (
    index,
    all_store_request,
    store_details,
    all_store,
    store_delete,
    store_details_update,
    store_deactive,
    store_active,
    store_deactived,
)

app_name='adminpanel'
urlpatterns = [
    path('',index,name='home'),
    path('store-request/',all_store_request,name='store_request'),
    path('store/',all_store,name='store'),
    path('store-deactived/',store_deactived,name='store_deactived'),
    path('store-details-update/<int:store_id>',store_details_update,name='store_details_update'),
    path('store-active/<int:store_id>',store_active,name='store_active'),
    path('store-deactive/<int:store_id>',store_deactive,name='store_deactive'),
    path('store-details/<int:store_id>',store_details,name='store_details'),
    path('store-delete/<int:store_id>',store_delete,name='store_delete'),
    #user urls
    path('user/',include('adminPanel.user.urls'),name='user')
]
