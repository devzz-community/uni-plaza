from rest_framework import serializers
from shop.models import Product, ProductCategory


class ProductSerializers(serializers.ModelSerializer):
    category = serializers.SlugRelatedField(slug_field='name', queryset=ProductCategory.objects.all())

    class Meta:
        model = Product
        fields = ('id', 'name', 'description', 'price', 'image', 'category')