from django.urls import path

from .views import (
    dev_home, 
    show_urls,
    show_phone_verification_table,
)

app_name = 'dev'
urlpatterns = [
    path('', dev_home, name='home'),
    path('urls/', show_urls, name='urls'),
    path('phone-verify-list/', show_phone_verification_table, name='phone-verify-list'),
]