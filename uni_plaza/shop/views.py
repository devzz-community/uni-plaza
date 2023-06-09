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
        'title': ProductCategory.objects.get(id=category_id),
        'products': Product.objects.filter(category=category_id),
        'categories': ProductCategory.objects.all()
    }
    return render(request, 'shop/products.html', context)


"""Открытие карточки товара"""


def product(request, category_id, product_id):
    context = {
        'title': ProductCategory.objects.get(id=category_id),
        'categories': ProductCategory.objects.all(),
        'product': Product.objects.filter(id=product_id)
    }
    return render(request, 'shop/product.html', context)
