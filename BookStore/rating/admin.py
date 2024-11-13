from django.contrib import admin
from .models import Rating , RatingResponse

class RatingAdmin(admin.ModelAdmin):
    list_display = ('user', 'product', 'rate', 'feed_back', 'isDelete')
    list_filter = ('rate', 'isDelete', 'user')
    search_fields = ('product__name', 'user__email', 'feed_back')

admin.site.register(Rating, RatingAdmin)
class RatingResponseAdmin(admin.ModelAdmin):
    # Cấu hình các trường hiển thị trong giao diện admin
    list_display = ('rating', 'user', 'response_text', 'created_at')
    search_fields = ('response_text', 'user__email', 'rating__product__name')
    list_filter = ('created_at', 'rating', 'user')
admin.site.register(RatingResponse, RatingResponseAdmin)