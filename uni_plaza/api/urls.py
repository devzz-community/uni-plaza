from django.urls import path, include
from api.views import ProductViewSet, ProductCategoryViewSet
from rest_framework import routers

app_name = 'api'

router = routers.DefaultRouter()
router.register(r'products', ProductViewSet)
router.register(r'catalogs', ProductCategoryViewSet)

urlpatterns = [
    path('', include(router.urls)),
]