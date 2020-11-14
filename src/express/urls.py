from django.urls import path

from .views import (
        express_home_view,
        register_merchant_view,
        merchant_billing_account_view,
        merchant_detail_view,
        merchant_update_view,
        merchant_parcel_list_view,
        merchant_parcel_add_view,
        merchant_parcel_detail_view,
        merchant_parcel_update_view,
        merchant_parcel_remove_view,
    )

app_name = 'express'
urlpatterns = [
    path('', express_home_view, name='home'),
    path('register/', register_merchant_view, name='register_merchant'),
    path('merchant/<str:merchant_username>/', merchant_detail_view, name='merchant_detail'),
    path('merchant/<str:merchant_username>/billing/account/', merchant_billing_account_view, name='merchant_billing_account'),
    path('merchant/<str:merchant_username>/update/', merchant_update_view, name='merchant_update'),
    path('merchant/<str:merchant_username>/parcels/', merchant_parcel_list_view, name='merchant_parcel_list'),
    path('merchant/<str:merchant_username>/parcels/add/', merchant_parcel_add_view, name='merchant_parcel_add'),
    path('merchant/<str:merchant_username>/parcels/<int:parcel_id>/', merchant_parcel_detail_view, name='merchant_parcel_detail'),
    path('merchant/<str:merchant_username>/parcels/<int:parcel_id>/update/', merchant_parcel_update_view, name='merchant_parcel_update'),
    path('merchant/<str:merchant_username>/parcels/<int:parcel_id>/remove/', merchant_parcel_remove_view, name='merchant_parcel_remove'),
]