from django.contrib import admin
from django import forms
from .models import Promotion

class PromotionAdminForm(forms.ModelForm):
    class Meta:
        model = Promotion
        fields = '__all__'

    class Media:
        js = ('promotion/js/promotion_admin.js',)  # Đảm bảo rằng tệp JavaScript được tải

class PromotionAdmin(admin.ModelAdmin):
    form = PromotionAdminForm
    list_display = ('name', 'discount_percent', 'start_date', 'end_date', 'is_active', 'promotion_type')
    list_filter = ('promotion_type', 'is_active', 'start_date', 'end_date')
    search_fields = ('name', 'description')
    filter_horizontal = ('subcategories', 'products')

    def save_model(self, request, obj, form, change):
        obj.save()
        form.save_m2m()

# Đăng ký mô hình Promotion với admin
admin.site.register(Promotion, PromotionAdmin)
