from django.shortcuts import render, HttpResponse


"""Главная страница"""
def index(request):
    return render(request, 'shop/base.html')


"""Товары"""
def products(request):
    return render(request, 'shop/products.html')


