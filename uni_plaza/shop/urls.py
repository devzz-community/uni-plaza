from django.urls import path
from shop.views import products, product, catalogs, search, basket_add, basket_remove

app_name = 'products'

urlpatterns = [
    # path('', products, name='index'),
    path('search/', search, name='search'),  # Поиск товаров
    path('basket/add/<int:product_id>/', basket_add, name='basket_add'),  # Добавление товара в корзину
    path('basket/remove/<int:basket_id>/', basket_remove, name='basket_remove'),  # Удаление товара из корзины
    path('', catalogs, name='catalogs'),
    path('<category_id>/', products, name='products'),
    path('<int:category_id>/<product_id>/', product, name='product'),

]
