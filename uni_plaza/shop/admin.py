from django import forms
from django.contrib import admin
from import_export.forms import ImportForm, ConfirmImportForm
from import_export.resources import ModelResource

from shop.models import ProductCategory, Product
from import_export import resources, fields
from import_export.widgets import ForeignKeyWidget
from import_export.admin import ImportExportModelAdmin, ImportMixin


# class CustomImportForm(ImportForm):
#     category = forms.ModelChoiceField(
#         queryset=ProductCategory.objects.all(),
#         required=True)
#
class CustomConfirmImportForm(ConfirmImportForm):
    category = forms.ModelChoiceField(
        queryset=ProductCategory.objects.all(),
        required=True)


# class ProductResource(resources.ModelResource):
#
#     def before_import_row(self, row, row_number=None, **kwargs):
#
#         row['category'] = 1
#
#
#
#     class Meta:
#         exclude = ('id',)
#         import_id_fields = ('name',)
#         model = Product


# class CustomProductAdmin(ImportMixin, admin.ModelAdmin):
#
#     import_form_class = CustomImportForm
#     confirm_form_class = CustomConfirmImportForm
#     resource_classes = [ProductResource]
#     list_display = ('name', 'price', 'category')
#
# def get_confirm_form_initial(self, request, import_form):
#     initial = super().get_confirm_form_initial(request, import_form)
#     # Pass on the `author` value from the import form to
#     # the confirm form (if provided)
#     if import_form:
#         initial['category'] = import_form.cleaned_data['category']
#         print(initial.get('category'))
#     return initial
#
#
# admin.site.register(Product, CustomProductAdmin)

class CategoryChoiceForm(ImportForm):
    category = forms.ModelChoiceField(
        queryset=ProductCategory.objects.all(),
        required=True
    )



""" Класс обработки данных """


class ProductResource(resources.ModelResource):

    def __init__(self, request=None):
        super()
        self.request = request

    # def before_import_row(self, row, **kwargs):
    #     category = self.request.POST.get('category', None)
        # if contract:
        #     self.request.session['import_context_category'] = category
        # else:
        #     # if this raises a KeyError, we want to know about it.
        #     # It means that we got to a point of importing data without
        #     # contract context, and we don't want to continue.
        #     try:
        #         category = self.request.session['import_context_category']
        #     except KeyError as e:
        #         raise Exception("Sector context failure on row import, " +
        #                         f"check resources.py for more info: {e}")
        # row['category'] = category

    def before_import_row(self, row, row_number=None, **kwargs):
        # print(self.request.POST.get('category', None))
        row['category'] = self.request.POST.get('category', None)

    class Meta:
        model = Product
        exclude = ('id',)
        import_id_fields = ('name',)


""" Вывод данных на странице """


class ProductAdmin(ImportExportModelAdmin):
    resource_classes = [ProductResource]
    import_form_class = CategoryChoiceForm
    confirm_form_class = CustomConfirmImportForm
    list_display = ('name', 'price', 'category')

    def get_resource_kwargs(self, request, *args, **kwargs):
        rk = super().get_resource_kwargs(request, *args, **kwargs)
        rk['request'] = request
        return rk

    # def get_confirm_form_initial(self, request, import_form):
    #     initial = super().get_confirm_form_initial(request, import_form)
    #     # Pass on the `author` value from the import form to
    #     # the confirm form (if provided)
    #     if import_form:
    #         initial['category'] = import_form.cleaned_data['category']
    #         print(initial.get('category'))
    #     return initial


admin.site.register(ProductCategory)
admin.site.register(Product, ProductAdmin)
