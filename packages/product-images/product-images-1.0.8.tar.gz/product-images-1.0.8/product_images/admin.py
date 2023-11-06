from django import forms
from django.contrib import admin
from django.utils.translation import gettext_lazy as _
from django.template.loader import render_to_string
from django.utils.safestring import mark_safe
from product_images.models import ProductImage

from product_images.fields import ImagesFormField


class ImagesForm(forms.ModelForm):

    images = ImagesFormField(label='')

    def __init__(self, *args, **kwargs):

        super(ImagesForm, self).__init__(*args, **kwargs)

        self.fields['images'].init_form(*args, **kwargs)

    def save(self, commit=True):
        instance = super().save(commit=commit)

        if commit:
            self.fields['images'].commit(instance)

        return instance


def get_logo_cell(product):
    images = list(product.images.all())
    return mark_safe(
        render_to_string("product-admin-preview.html", {
            "product": product,
            "images": images
        })
    )


@admin.register(ProductImage)
class UnlinkedProductImageAdmin(admin.ModelAdmin):

    list_display = ['id', 'order', 'created', 'preview_cell']
    list_per_page = 100

    def get_queryset(self, request):
        return super().get_queryset(request).filter(product__isnull=True)

    @admin.display(description=_('Preview'))
    def preview_cell(self, obj):
        return render_to_string('admin/list_item_preview.html', {
            'file': obj.file
        })
