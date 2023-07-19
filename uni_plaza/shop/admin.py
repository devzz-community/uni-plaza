from django.contrib import admin
from shop.models import ProductCategory, Product, Basket
from import_export import resources
from import_export.admin import ImportExportModelAdmin
from shop.forms import CategoryChoiceForm, CategoryConfirmImportForm


""" Класс обработки данных """


class ProductResource(resources.ModelResource):

    def __init__(self, request=None):
        super()
        self.request = request

    def before_import_row(self, row, row_number=None, **kwargs):
        row['category'] = self.request.POST.get('category', None)

    class Meta:
        model = Product
        exclude = ('id',)
        import_id_fields = ('name',)


""" Вывод данных на странице """


class ProductAdmin(ImportExportModelAdmin):
    resource_classes = [ProductResource]
    import_form_class = CategoryChoiceForm
    confirm_form_class = CategoryConfirmImportForm
    list_display = ('name', 'price', 'category')

    def get_resource_kwargs(self, request, *args, **kwargs):
        rk = super().get_resource_kwargs(request, *args, **kwargs)
        rk['request'] = request
        return rk

    def get_confirm_form_initial(self, request, import_form):
        initial = super().get_confirm_form_initial(request, import_form)
        # Передает значение категории из формы импорта в
        # форму подтверждения (если есть)
        if import_form:
            initial['category'] = import_form.cleaned_data['category']
            print(initial.get('category'))
        return initial


admin.site.register(ProductCategory)
admin.site.register(Product, ProductAdmin)
admin.site.register(Basket)
