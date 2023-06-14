from django.shortcuts import render, HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from shop.models import ProductCategory, Product, Basket
from users.models import User

""" Главная страница с категориями """


def index(request):
    context = {
        'title': 'Магазин',
        'categories': ProductCategory.objects.all()
    }
    return render(request, 'shop/index.html', context)


""" Товары """


def products(request, category_id):
    context = {
        'title': ProductCategory.objects.get(id=category_id),
        'products': Product.objects.filter(category=category_id),
        'categories': ProductCategory.objects.all()
    }
    return render(request, 'shop/products.html', context)


""" Открытие карточки товара """


def product(request, category_id, product_id):
    context = {
        'title': ProductCategory.objects.get(id=category_id),
        'categories': ProductCategory.objects.all(),
        'product': Product.objects.filter(id=product_id)
    }
    return render(request, 'shop/product.html', context)


""" Строка поиска """


def search(request):
    search_query = request.GET.get('q', '')
    context = {
        'title': 'Магазин',
        'categories': ProductCategory.objects.all(),
        'products': Product.objects.filter(name__icontains=search_query),
    }
    return render(request, 'shop/search.html', context)


""" Добавление товара в корзину """


@login_required
def basket_add(request, product_id):
    product = Product.objects.get(id=product_id)
    baskets = Basket.objects.filter(user=request.user, product=product)

    if not baskets.exists():
        Basket.objects.create(user=request.user, product=product, quantity=1)
    else:
        baskets = baskets.first()
        baskets.quantity += 1
        baskets.save()

    return HttpResponseRedirect(request.META['HTTP_REFERER'])


""" Удаление товара из корзины """


@login_required
def basket_remove(request, basket_id):
    basket = Basket.objects.get(id=basket_id)
    basket.delete()
    return HttpResponseRedirect(request.META['HTTP_REFERER'])
