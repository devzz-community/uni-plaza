from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAdminUser
from shop.models import Product
from shop.serializers import ProductSerializers


class ProductViewSet(ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializers

    def get_permissions(self):
        if self.action in ('create', 'update', 'destroy'):
            self.permission_classes = (IsAdminUser,)
        return super(ProductViewSet, self).get_permissions()