from orders.models import Order
from rest_framework.viewsets import ModelViewSet
from orders.serializers import OrderSerializer
from rest_framework.permissions import IsAuthenticated


class OrderViewSet(ModelViewSet):
    """
    Оформление заказа
    """
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    permission_classes = (IsAuthenticated,)
