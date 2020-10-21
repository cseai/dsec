from django.urls import path

from .views import (
    dev_home, 
    show_urls,
)

app_name = 'dev'
urlpatterns = [
    path('', dev_home, name='home'),
    path('urls/', show_urls, name='urls'),
]