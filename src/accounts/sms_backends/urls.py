# In urls.py

from rest_framework.routers import DefaultRouter
from phone_verify.api import VerificationViewSet

default_router = DefaultRouter(trailing_slash=False)
default_router.register('phone', VerificationViewSet, basename='phone')

urlpatterns = default_router.urls
