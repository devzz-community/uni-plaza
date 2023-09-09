from django.urls import path, include
from users.views import ActivateUser, UserViewSet, LoginView
from rest_framework import routers
from uni_plaza.yasg import DecoratedTokenBlacklistView

app_name = 'users'

router = routers.DefaultRouter()
router.register(r'admin', UserViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('activate/<uid>/<token>', ActivateUser.as_view({'get': 'activation'}), name='activation'),
    path('login/', LoginView.as_view(), name='login'),

    path('', include('djoser.urls')),
    path('', include('djoser.urls.jwt')),


    path('logout/', DecoratedTokenBlacklistView.as_view(), name='token_blacklist'),
]
