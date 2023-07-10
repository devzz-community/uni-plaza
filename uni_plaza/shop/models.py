from django.db import models
from users.models import User


class ProductCategory(models.Model):
    """
    Категории товаров
    """
    name = models.CharField(max_length=128, unique=True)  # Название
    description = models.TextField(null=True, blank=True)  # Описание
    image = models.ImageField(upload_to='category_images', null=True)  # Изображение

    def __str__(self):
        return self.name


class Product(models.Model):
    """
    Товары
    """
    name = models.CharField(max_length=256)  # Наименование
    description = models.TextField(null=True, blank=True)  # Описание
    price = models.DecimalField(max_digits=8, decimal_places=2)  # Цена
    image = models.ImageField(upload_to='products_images', null=True)  # Изображение
    category = models.ForeignKey(to=ProductCategory, on_delete=models.PROTECT)  # Ссылка на категорию

    def __str__(self):
        return self.name


class BasketQuerySet(models.QuerySet):
    """
    Новый менеджер для обращения ко всем объектам корзины
    """

    def total_sum(self):
        return sum(basket.sum() for basket in self)

    def total_quantity(self):
        return sum(basket.quantity for basket in self)


class Basket(models.Model):
    """
    Корзина товаров
    """
    user = models.ForeignKey(to=User, on_delete=models.CASCADE)
    product = models.ForeignKey(to=Product, on_delete=models.CASCADE)
    quantity = models.PositiveSmallIntegerField(default=0)

    objects = BasketQuerySet.as_manager()

    def __str__(self):
        return f'Корзина для: {self.user.name} | Товар: {self.product.name}'

    def sum(self):
        return self.product.price * self.quantity
