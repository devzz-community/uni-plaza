from django.urls import path, include
from shop.views import ProductCategoryViewSet, ProductViewSet, BasketViewSet, ProductList
from rest_framework import routers

app_name = 'products'

router = routers.DefaultRouter()
router.register(r'products', ProductViewSet)
router.register(r'catalogs', ProductCategoryViewSet)
router.register(r'baskets', BasketViewSet)


urlpatterns = [
    path('', include(router.urls)),
    path('search/', ProductList.as_view(), name='search'),  # Поиск товаров

]
