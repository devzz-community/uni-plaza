from django.shortcuts import render
from shop.models import ProductCategory, Product

"""Главная страница с категориями"""


def index(request):
    context = {
        'title': 'Магазин',
        'categories': ProductCategory.objects.all()
    }
    return render(request, 'shop/index.html', context)


"""Товары"""


def products(request, category_id):
    context = {
        'title': 'Категория',
        'products': Product.objects.filter(category=category_id),
        'categories': ProductCategory.objects.all()
    }
    return render(request, 'shop/products.html', context)
