from django.db import models

""" Категории товаров """


class ProductCategory(models.Model):
    name = models.CharField(max_length=128, unique=True)  # Название
    description = models.TextField(null=True, blank=True)  # Описание
    image = models.ImageField(upload_to='category_images')  # Изображение

    def __str__(self):
        return self.name


""" Товары """


class Product(models.Model):
    name = models.CharField(max_length=256)  # Наименование
    description = models.TextField(null=True, blank=True)  # Описание
    price = models.DecimalField(max_digits=6, decimal_places=2)  # Цена
    image = models.ImageField(upload_to='products_images')  # Изображение
    category = models.ForeignKey(to=ProductCategory, on_delete=models.PROTECT)  # Ссылка на категорию

    def __str__(self):
        return self.name
