"""uni_plaza URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
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
from django.contrib import admin
from django.urls import path, re_path, include
from django.conf.urls.static import static
from django.conf import settings
from .yasg import urlpatterns as doc_urls
from .yasg import (DecoratedTokenObtainPairView,
                   DecoratedTokenRefreshView,
                   DecoratedTokenVerifyView,
                   DecoratedTokenBlacklistView)

from shop.views import IndexView


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', IndexView.as_view(), name='index'),
    path('products/', include('shop.urls', namespace='products')),
    path('users/', include('users.urls', namespace='users')),
    path('orders/', include('orders.urls', namespace='orders')),
    path('api/', include('api.urls', namespace='api')),
    path('auth/', include('djoser.urls')),

    path('api/token/', DecoratedTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', DecoratedTokenRefreshView.as_view(), name='token_refresh'),
    path('api/token/verify/', DecoratedTokenVerifyView.as_view(), name='token_verify'),
    path('api/token/blacklist/', DecoratedTokenBlacklistView.as_view(), name='token_blacklist'),
]

urlpatterns += doc_urls

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
