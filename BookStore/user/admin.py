from django.contrib import admin
from .models import Role , Account , UserToken
from django.contrib.auth.models import Group
from django.utils.safestring import mark_safe

admin.site.site_header = "Bookstore Admin"  # Tiêu đề trên đầu trang
admin.site.site_title = "Bookstore Admin Portal"  # Tiêu đề của tab
admin.site.index_title = "Chào mừng bạn đến với Admin của Bookstore"  # Tiêu đề chính
# Register your models here.
@admin.register(Account)
class AccountAdmin(admin.ModelAdmin):
    list_display = ('image_tag','username', 'email', 'phone', 'status', 'role', 'is_staff', 'is_superuser')
    list_filter = ('status', 'role', 'is_staff', 'is_superuser')
    search_fields = ('username', 'email', 'phone')
    readonly_fields = ('last_login', 'date_joined')  # Chỉ đặt các trường không cần chỉnh sửa ở đây

    # Thêm tùy chỉnh fieldsets để sắp xếp các trường trong trang chi tiết
    fieldsets = (
        (None, {
            'fields': ('username',)
        }),
        ('Thông tin cá nhân', {
            'fields': ('email', 'phone', 'address', 'status','image')
        }),
        ('Thông tin quyền', {
            'fields': ('role', 'is_staff', 'is_superuser', 'is_active')
        }),
        ('Các mốc thời gian', {
            'fields': ('last_login', 'date_joined'),
            'classes': ('collapse',),
        }),
    )
    def image_tag(self, obj):
        if obj.image:
            return mark_safe(f'<img src="{obj.image.url}" width="50" height="50" />')  # Hiển thị ảnh thu nhỏ 50x50px
        return "No Image"  # Trường hợp không có ảnh

    image_tag.short_description = 'Hình ảnh'

@admin.register(Role)
class RoleAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)

@admin.register(UserToken)
class UserTokenAdmin(admin.ModelAdmin):
    list_display = ('user', 'created_at')
    search_fields = ('user__email',)
    readonly_fields = ('created_at',)
admin.site.unregister(Group)