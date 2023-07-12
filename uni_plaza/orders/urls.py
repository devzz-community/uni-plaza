from django.urls import path
from orders.views import OrderViewSet

app_name = 'orders'

urlpatterns = [
    path('order_create/', OrderViewSet.as_view({'post': 'create'}), name='order_create'),
]
