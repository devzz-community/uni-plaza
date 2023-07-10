from django.shortcuts import HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from shop.models import ProductCategory, Product, Basket
from django.views.generic.list import ListView
from common.views import TitleMixin
from rest_framework.viewsets import ModelViewSet
from shop.serializers import ProductSerializers, ProductCategorySerializers
from rest_framework.permissions import IsAdminUser


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


""" Строка поиска """


class SearchView(TitleMixin, ListView):
    model = Product
    template_name = 'shop/search.html'
    title = 'Результаты поиска'

    def get_queryset(self):
        return Product.objects.filter(name__icontains=self.request.GET.get('q'))

    def get_context_data(self, **kwargs):
        context = super(SearchView, self).get_context_data(**kwargs)
        context['products'] = self.request.GET.get('q')
        context['categories'] = ProductCategory.objects.all()
        return context


""" Добавление товара в корзину """


@login_required
def basket_add(request, product_id):
    product = Product.objects.get(id=product_id)
    baskets = Basket.objects.filter(user=request.user, product=product)

    if not baskets.exists():
        Basket.objects.create(user=request.user, product=product, quantity=1)
    else:
        basket = baskets.first()
        basket.quantity += 1
        basket.save()

    return HttpResponseRedirect(request.META['HTTP_REFERER'])


""" Удаление товара из корзины """


@login_required
def basket_remove(request, basket_id):
    basket = Basket.objects.get(id=basket_id)
    basket.delete()
    return HttpResponseRedirect(request.META['HTTP_REFERER'])
