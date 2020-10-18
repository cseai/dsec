from django.urls import path

from accounts.views import (
        AccountHomeView,
    )

app_name = 'accounts'
urlpatterns = [
    path('', AccountHomeView.as_view(), name='account'),
]