from django.contrib import admin
from shop.models import ProductCategory, Product
from import_export import resources
from import_export.admin import ImportExportModelAdmin

""" Класс обработки данных """


class ProductResource(resources.ModelResource):
    class Meta:
        model = Product


""" Вывод данных на странице """


class ProductAdmin(ImportExportModelAdmin):
    resource_classes = [ProductResource]


admin.site.register(ProductCategory)
admin.site.register(Product, ProductAdmin)
