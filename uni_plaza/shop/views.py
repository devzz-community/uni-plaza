from django.shortcuts import render, HttpResponse

def index(request):
    return render(request, 'shop/base.html')

def products(request):
    return render(request, 'shop/products.html')


