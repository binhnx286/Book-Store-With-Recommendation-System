from django.contrib import admin
from .models import Product, Category, SubCategory
from ckeditor.widgets import CKEditorWidget
from django import forms
from django.utils.safestring import mark_safe


class ProductAdminForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = '__all__'
        widgets = {
            'description': CKEditorWidget(),
        }

class ProductSearchForm(forms.Form):
    search_term = forms.CharField(label='Tìm kiếm', required=False)
@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    form = ProductAdminForm
    list_display = ('name', 'image_tag', 'price_origin', 'new_price', 'quantity', 'viewed', 'sub_category', 'is_delete')
    list_filter = ('is_delete', 'sub_category', 'publication_year')
    search_fields = ('name__icontains', 'author__icontains', 'publisher__icontains')
    readonly_fields = ('discount_percent',)
    list_per_page = 20
    def changelist_view(self, request, extra_context=None):
        extra_context = extra_context or {}
        
        return super().changelist_view(request, extra_context=extra_context)

    def mark_as_deleted(self, request, queryset):
        queryset.update(is_delete=True)
        self.message_user(request, f"{queryset.count()} sản phẩm đã được đánh dấu là đã xóa.")
    mark_as_deleted.short_description = "Đánh dấu sản phẩm đã xóa"

    def image_tag(self, obj):
        return mark_safe(f'<img src="{obj.image}" width="50" height="50" />')
    image_tag.short_description = 'Hình ảnh'


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'is_delete')
    search_fields = ('name',)


@admin.register(SubCategory)
class SubCategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'is_delete')
    search_fields = ('name',)
    list_filter = ('category',)
