from django.contrib import admin

from users.models import User

"""Регистрируем модель в админ панели"""
admin.site.register(User)
