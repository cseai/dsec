from django.urls import path
from django.contrib.auth.views import LogoutView

from .views import (
        LoginView, 
        verify_then_redirect_register,
        verify_and_register,
    )
 
app_name = 'auth'
urlpatterns = [
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    # phone verification and register
    path('register/', verify_then_redirect_register, name='register'),
    path('register/<str:phone_number>/<int:security_code>/<str:session_token>/', verify_and_register, name='verify_and_register'),
]