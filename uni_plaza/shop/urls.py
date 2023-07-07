from django.urls import path
from shop.views import ProductsListView, ProductListView, CatalogListView, SearchView, basket_add, basket_remove
from api.views import ProductCategoryViewSet

app_name = 'products'

urlpatterns = [
    path('search/', SearchView.as_view(), name='search'),  # Поиск товаров
    path('basket/add/<int:product_id>/', basket_add, name='basket_add'),  # Добавление товара в корзину
    path('basket/remove/<int:basket_id>/', basket_remove, name='basket_remove'),  # Удаление товара из корзины
    # path('', CatalogListView.as_view(), name='catalogs'),
    # path('', ProductCategoryViewSet.as_view({'get': 'list'}), name='catalogs'),
    path('<int:category_id>/', ProductsListView.as_view(), name='products'),
    path('<int:category_id>/<int:product_id>/', ProductListView.as_view(), name='product'),

]
