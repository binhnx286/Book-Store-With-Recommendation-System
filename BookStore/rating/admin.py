from django.contrib import admin
from .models import Rating

class RatingAdmin(admin.ModelAdmin):
    list_display = ('user', 'product', 'rate', 'feed_back', 'isDelete')
    list_filter = ('rate', 'isDelete', 'user')
    search_fields = ('product__name', 'user__email', 'feed_back')

admin.site.register(Rating, RatingAdmin)
