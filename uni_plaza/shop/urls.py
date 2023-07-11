from django.urls import path, include
from shop.views import ProductCategoryViewSet, ProductViewSet, BasketViewSet
from rest_framework import routers

app_name = 'products'

router = routers.DefaultRouter()
router.register(r'products', ProductViewSet)
router.register(r'catalogs', ProductCategoryViewSet)
router.register(r'baskets', BasketViewSet)

urlpatterns = [
    path('', include(router.urls)),
    # path('search/', SearchView.as_view(), name='search'),  # Поиск товаров
    # path('basket/add/<int:product_id>/', basket_add, name='basket_add'),  # Добавление товара в корзину
    # path('basket/remove/<int:basket_id>/', basket_remove, name='basket_remove'),  # Удаление товара из корзины

]
