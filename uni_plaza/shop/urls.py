from django.urls import path
from shop.views import products, product

app_name = 'products'

urlpatterns = [
    # path('', products, name='index'),
    path('<category_id>/', products, name='products'),
    path('<int:category_id>/<product_id>/', product, name='product'),
]
