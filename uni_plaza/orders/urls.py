from django.urls import path, include
from rest_framework import routers
from orders.views import OrderViewSet

app_name = 'orders'

router = routers.DefaultRouter()
router.register(r'order', OrderViewSet)

urlpatterns = [
    # path('order_create/', OrderViewSet.as_view({'post': 'create'}), name='order_create'),
    path('', include(router.urls)),
]
