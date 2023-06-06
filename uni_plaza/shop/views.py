from django.shortcuts import render
from shop.models import ProductCategory, Product

"""Главная страница с категориями"""


def index(request):
    context = {
        'title': 'Магазин',
        'categories': ProductCategory.objects.all()
    }
    return render(request, 'shop/base.html', context)


"""Товары"""


def products(request):
    context = {
        'title': 'Категория',
        'products': Product.objects.all(),
        'categories': ProductCategory.objects.all()
    }
    return render(request, 'shop/products.html', context)
