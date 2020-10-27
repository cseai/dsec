from django.urls import path
from django.contrib.auth.views import LogoutView

from .views import (
        LoginView,  
        RegisterView,
        verify_phone,
        show_phone_verification_table,
        # verify_then_register,
        verify_then_redirect_register,
        verify_and_register,
    )
 
app_name = 'auth'
urlpatterns = [
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('register/', RegisterView.as_view(), name='register'),

    # phone verification
    path('verify/', verify_phone, name='verify'),
    path('phone-list/', show_phone_verification_table, name='phone_list'),
    # path('verify-register/', verify_then_register, name='verify_then_register'),
    path('verify-register/', verify_then_redirect_register, name='verify_then_redirect_register'),
    path('verify-register/<str:phone_number>/<int:security_code>/<str:session_token>/', verify_and_register, name='verify_and_register'),
]