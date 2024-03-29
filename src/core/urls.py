"""core URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf import settings
from django.conf.urls import include
from django.conf.urls.static import static

from django.contrib import admin
from django.urls import path

import notifications.urls

urlpatterns = [
    path('', include('home.urls')),
    path('stores/', include('home.stores.urls')),
    path('admin/', admin.site.urls),    
    path('auth/', include('accounts.auth.urls')),
    path('profile/', include('profiles.urls')),
    path('express/', include("express.urls")),
    path('vendor/', include("vendors.urls")),
    path('adminpanel/', include('adminPanel.urls')),
    # Notifications
    path('notifications/', include(notifications.urls, namespace='notifications')),
    # api
    path('api/phone-verify/', include('accounts.sms_backends.urls')),
    # Devlopments only
    path('dev/', include('home.dev.urls')),
]


if settings.DEBUG:
    urlpatterns = urlpatterns + \
        static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns = urlpatterns + \
        static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
