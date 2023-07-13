from shop.models import ProductCategory, Product, Basket
from rest_framework import status, generics
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from shop.serializers import ProductSerializers, ProductCategorySerializers, BasketSerializers
from rest_framework.permissions import IsAdminUser, IsAuthenticated, AllowAny
from django_filters import rest_framework as filters


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


class BasketViewSet(ModelViewSet):
    """
    Корзина товаров
    """
    queryset = Basket.objects.all()
    serializer_class = BasketSerializers
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        queryset = super(BasketViewSet, self).get_queryset()
        return queryset.filter(user=self.request.user)

    def create(self, request, *args, **kwargs):
        try:
            product_id = request.data['product_id']
            products = Product.objects.filter(id=product_id)
            if not products.exists():
                return Response({'product_id': 'There is no product with this ID.'}, status=status.HTTP_400_BAD_REQUEST)
            obj, is_created = Basket.create_or_update(products.first().id, self.request.user)
            status_code = status.HTTP_201_CREATED if is_created else status.HTTP_200_OK
            serializer = self.get_serializer(obj)
            return Response(serializer.data, status=status_code)
        except KeyError:
            return Response({'product_id': 'This field is required.'}, status=status.HTTP_400_BAD_REQUEST)


class ProductFilter(filters.FilterSet):
    """
    Фильтр поиска продуктов
    """
    name = filters.CharFilter(field_name="name", lookup_expr='icontains')
    category = filters.CharFilter(field_name="category__name", lookup_expr='icontains')

    class Meta:
        model = Product
        fields = ['category']


class ProductList(generics.ListAPIView):
    """
    Поиск продуктов по названию
    """
    queryset = Product.objects.all()
    serializer_class = ProductSerializers
    filter_backends = (filters.DjangoFilterBackend,)
    filterset_class = ProductFilter
