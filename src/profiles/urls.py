from django.urls import path

from .views import (
    user_profile_home_view,
    user_profile_update_view,
)

app_name = 'profiles'
urlpatterns = [
    path('', user_profile_home_view, name='profile'),
    path('update/', user_profile_update_view, name='profile_update'),
]