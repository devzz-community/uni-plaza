from django.shortcuts import render


"""Вход пользователя"""
def login(request):
    return render(request, 'users/login.html')

"""Регистрация пользователя"""
def register(request):
    return render(request, 'users/register.html')
