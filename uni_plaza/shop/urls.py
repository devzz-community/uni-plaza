from django.urls import path
from shop.views import products

app_name = 'products'

urlpatterns = [
    # path('', products, name='index'),
    path('<category_id>/', products, name='products' ),
]