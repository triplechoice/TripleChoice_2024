from django.contrib import admin
from django.core.exceptions import ValidationError
from django.urls import reverse
from django.utils.html import format_html
from django.contrib.auth import get_user_model
from django.forms.models import BaseInlineFormSet

from product.forms.part_supplier_forms import PartSupplierForm
from product.models.product_models import *

User = get_user_model()


class ClassificationAdminForm(BaseInlineFormSet):
    def clean(self):
        super(ClassificationAdminForm, self).clean()
        items = []
        for form in self.forms:
            if str(form.cleaned_data.get('title')) != "None":
                items.append(str(form.cleaned_data.get('title')).lower())

        for item in items:
            count = 0
            for form in self.forms:
                if str(form.cleaned_data.get('title')).lower() == item:
                    count += 1
                if count > 1:
                    form.add_error('title', "Duplicate")
                    raise ValidationError(' ')


class AttributeInlineAdmin(admin.TabularInline):
    model = Attribute
    extra = 0
    formset = ClassificationAdminForm


@admin.register(Classification)
class ClassificationAdmin(admin.ModelAdmin):
    inlines = (AttributeInlineAdmin,)


@admin.register(Part)
class PartAdmin(admin.ModelAdmin):
    add_form_template = 'admin/product/create.html'
    change_form_template = 'admin/product/update.html'
    list_display = ['title', 'classification', 'action']
    search_fields = ['title']

    def classification(self, obj: Part):
        """
        part classification name
        @param obj:
        @return:
        """
        return list(obj.partclassification_set.values_list('classification__title'))

    @admin.action(description='Action')
    def action(self, obj: PartSupplier):
        part_existence = PartSupplier.objects.filter(part_id=obj.id).first()
        if part_existence:
            button = format_html(
                f'<a class="button" '
                f'href="{reverse("admin:product_partsupplier_change", args=[part_existence.id])}">'
                f'Add Supplier</a>&nbsp;'
            )
        else:
            button = format_html(
                f'<a class="button" '
                f'href="{reverse("admin:product_partsupplier_add")}">'
                f'Add Supplier</a>&nbsp;'
            )
        return button


@admin.register(PartSupplier)
class PartSupplierAdmin(admin.ModelAdmin):
    change_form_template = 'admin/product/part_supplier/create.html'
    add_form_template = 'admin/product/part_supplier/create.html'
    list_display = ['part', 'suppliers']
    search_fields = ['part__title']
    list_per_page = 50
    form = PartSupplierForm

    def suppliers(self, obj: PartSupplier):
        return list(obj.supplier.values_list('username', flat=True))

    def change_view(self, request, object_id, form_url='', extra_context=None):
        extra_context = extra_context or {}
        extra_context['form'] = self.form(instance=PartSupplier.objects.get(id=object_id))
        extra_context['change'] = True
        extra_context['object_id'] = object_id
        return super(PartSupplierAdmin, self).change_view(
            request, object_id, form_url, extra_context=extra_context,
        )

    def add_view(self, request, form_url='', extra_context=None):
        extra_context = {
            "form": self.form
        }
        return self.changeform_view(request, None, form_url, extra_context)
