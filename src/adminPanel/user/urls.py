from django.urls import path
from adminPanel.user.views import (
    all_user,user_details,
    user_details_update
)
app_name='adminpanel_user'

urlpatterns = [
    path('',all_user,name='all_user'),
    path('user-details/<int:user_id>',user_details,name='user_details'),
    path('user-details-update/<int:user_id>',user_details_update,name='user_details_update'),
]
