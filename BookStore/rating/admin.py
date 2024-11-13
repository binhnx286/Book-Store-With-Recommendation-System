from django.contrib import admin
from .models import Rating , RatingResponse

class RatingAdmin(admin.ModelAdmin):
    # Hiển thị các trường trong danh sách
    list_display = ('user', 'product', 'rate', 'feed_back', 'isDelete', 'is_disabled')
    
    # Bộ lọc cho các trường
    list_filter = ('rate', 'isDelete', 'user', 'is_disabled')
    
    # Các trường tìm kiếm trong admin
    search_fields = ('product__name', 'user__email', 'feed_back')

    # Sắp xếp theo các trường nhất định
    ordering = ('-rate',)  # Sắp xếp theo `rate` giảm dần
    
    # Các hành động tùy chỉnh
    actions = ['disable_ratings', 'enable_ratings']

    def disable_ratings(self, request, queryset):
        """Hành động tắt phản hồi (disable) cho các đánh giá đã chọn"""
        queryset.update(is_disabled=True)
        self.message_user(request, "Đã tắt phản hồi cho các đánh giá đã chọn.")

    def enable_ratings(self, request, queryset):
        """Hành động bật phản hồi (enable) cho các đánh giá đã chọn"""
        queryset.update(is_disabled=False)
        self.message_user(request, "Đã bật phản hồi cho các đánh giá đã chọn.")

    disable_ratings.short_description = "Tắt phản hồi"
    enable_ratings.short_description = "Bật phản hồi"

# Đăng ký mô hình và admin vào Django admin
admin.site.register(Rating, RatingAdmin)
class RatingResponseAdmin(admin.ModelAdmin):
    # Cấu hình các trường hiển thị trong giao diện admin
    list_display = ('rating', 'user', 'response_text', 'created_at')
    search_fields = ('response_text', 'user__email', 'rating__product__name')
    list_filter = ('created_at', 'rating', 'user')
admin.site.register(RatingResponse, RatingResponseAdmin)