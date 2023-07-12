from rest_framework import serializers, fields
from shop.models import Product, ProductCategory, Basket


class ProductCategorySerializers(serializers.ModelSerializer):
    """ Список категорий товаров """

    class Meta:
        model = ProductCategory
        fields = ('id', 'name', 'image')


class ProductSerializers(serializers.ModelSerializer):
    """ Список продуктов """
    category = serializers.SlugRelatedField(slug_field='name', queryset=ProductCategory.objects.all())

    class Meta:
        model = Product
        fields = ('id', 'name', 'description', 'price', 'image', 'category')


class BasketSerializers(serializers.ModelSerializer):
    """
    Корзина пользователя
    """
    product = ProductSerializers()
    sum = fields.FloatField(required=False)
    total_sum = fields.SerializerMethodField()
    total_quantity = fields.SerializerMethodField()

    class Meta:
        model = Basket
        fields = ('id', 'product', 'quantity', 'sum', 'total_sum', 'total_quantity')

    def get_total_sum(self, obj):
        return Basket.objects.filter(user_id=obj.user.id).total_sum()

    def get_total_quantity(self, obj):
        return Basket.objects.filter(user_id=obj.user.id).total_quantity()
