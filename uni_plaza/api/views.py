from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAdminUser
from rest_framework import generics
from shop.models import Product, ProductCategory
from shop.serializers import ProductSerializers, ProductCategorySerializers


class ProductCategoryViewSet(ModelViewSet):
    """ Категории товаров """
    queryset = ProductCategory.objects.all()
    serializer_class = ProductCategorySerializers

    def get_permissions(self):
        if self.action in ('create', 'update', 'destroy'):
            self.permission_classes = (IsAdminUser,)
        return super(ProductCategoryViewSet, self).get_permissions()


class ProductViewSet(ModelViewSet):
    """ Работа с товарами """
    queryset = Product.objects.all()
    serializer_class = ProductSerializers

    def get_permissions(self):
        if self.action in ('create', 'update', 'destroy'):
            self.permission_classes = (IsAdminUser,)
        return super(ProductViewSet, self).get_permissions()





