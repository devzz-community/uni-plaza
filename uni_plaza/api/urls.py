from django.urls import path, include
from api.views import ProductViewSet
from rest_framework import routers

app_name = 'api'

router = routers.DefaultRouter()
router.register(r'products', ProductViewSet)

urlpatterns = [
    path('', include(router.urls)),
]