from rest_framework import serializers
from shop.models import Product, ProductCategory
from djoser.serializers import UserCreateSerializer


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



