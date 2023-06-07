from django.db import models
from django.contrib.auth.models import AbstractUser


"""Расширяем модель пользователя"""
class User(AbstractUser):
    image = models.ImageField(upload_to='users_images', null=True, blank=True)


