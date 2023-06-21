from import_export.forms import ImportForm, ConfirmImportForm
from shop.models import ProductCategory
from django import forms


""" Форма выбора категории перед импортом """


class CategoryChoiceForm(ImportForm):
    category = forms.ModelChoiceField(
        queryset=ProductCategory.objects.all(),
        required=True
    )


""" Форма подтверждения категории при предварительном просмотре """


class CategoryConfirmImportForm(ConfirmImportForm):
    category = forms.ModelChoiceField(
        queryset=ProductCategory.objects.all(),
        required=True
    )
