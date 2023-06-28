from django.shortcuts import render, HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from shop.models import ProductCategory, Product, Basket
from django.views.generic.base import TemplateView
from django.views.generic.list import ListView
from common.views import TitleMixin

""" Главная страница с категориями """


class IndexView(TitleMixin, TemplateView):
    template_name = 'shop/index.html'
    title = 'Магазин'

    def get_context_data(self, **kwargs):
        context = super(IndexView, self).get_context_data()
        context['categories'] = ProductCategory.objects.all()
        return context


""" Каталоги """


class CatalogListView(TitleMixin, ListView):
    model = ProductCategory
    template_name = 'shop/catalogs.html'
    title = 'Каталоги товаров'


""" Товары """


class ProductsListView(ListView):
    model = Product
    template_name = 'shop/products.html'

    # paginate_by = 9

    def get_queryset(self):
        queryset = super(ProductsListView, self).get_queryset()
        category_id = self.kwargs.get('category_id')
        return queryset.filter(category_id=category_id) if category_id else queryset

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(ListView, self).get_context_data()
        context['title'] = ProductCategory.objects.get(id=self.kwargs['category_id'])
        context['categories'] = ProductCategory.objects.all()
        return context


""" Открытие карточки товара """


class ProductListView(ListView):
    model = Product
    template_name = 'shop/product.html'

    def get_queryset(self):
        queryset = super(ProductListView, self).get_queryset()
        product_id = self.kwargs.get('product_id')
        return queryset.filter(id=product_id) if product_id else queryset

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(ListView, self).get_context_data()
        context['title'] = Product.objects.get(id=self.kwargs['product_id'])
        context['categories'] = ProductCategory.objects.all()
        return context


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
