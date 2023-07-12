from rest_framework import serializers
from orders.models import Order
from shop.models import Basket


class OrderSerializer(serializers.ModelSerializer):
    """
    Создание заказа пользователя
    """

    class Meta:
        model = Order
        fields = ('first_name', 'last_name', 'email', 'address', 'basket_history')

    def create(self, validated_data):
        validated_data['initiator_id'] = self.context['request'].auth.payload['user_id']
        basket_history = Basket.objects.filter(user_id=validated_data['initiator_id'])
        line_items = []
        for basket in basket_history:
            item = {
                'product': basket.product.name,
                'price': str(basket.product.price),
                'quantity': basket.quantity,
            }
            line_items.append(item)
        validated_data['basket_history'] = line_items
        return Order.objects.create(**validated_data)
