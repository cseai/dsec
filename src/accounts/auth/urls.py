from django.urls import path
from django.contrib.auth.decorators import login_required

from django.contrib.auth.views import (
        LogoutView, 
        PasswordChangeView, 
        PasswordChangeDoneView,
    )

from .views import (
        LoginView,
        verify_then_redirect_register,
        verify_and_register,
        verify_then_redirect_password_reset,
        verify_and_password_reset,
        password_reset_done,
        password_reset_failed,
    )
 
app_name = 'auth'
urlpatterns = [
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),

    # phone verification and register
    path('register/', verify_then_redirect_register, name='register'),
    path('register/<str:phone_number>/<str:security_code>/<str:session_token>/', 
        verify_and_register, 
        name='verify_and_register'
    ),

    # password change
    path('password-change/', 
        login_required(PasswordChangeView.as_view(
            template_name='auth/password_change.html',
            success_url='/auth/password-change/done/'
        )), 
        name='password_change'
    ),
    path('password-change/done/', 
        login_required(PasswordChangeDoneView.as_view(
            template_name='auth/password_change_done.html'
        )), 
        name='password_change_done'
    ),

    # passwor reset by phone OTP
    path('password-reset/', verify_then_redirect_password_reset, name='password_reset'),
    path('password-reset/<str:phone_number>/<str:security_code>/<str:session_token>/', 
        verify_and_password_reset, 
        name='password_reset_confirm'
    ),
    path('password-reset/done/', password_reset_done, name='password_reset_done'),
    path('password-reset/failed/', password_reset_failed, name='password_reset_failed'),
]