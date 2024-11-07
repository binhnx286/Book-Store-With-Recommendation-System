from django.contrib import admin
from .models import Order, OrderDetail, Cart, CartItem, Voucher

# Đăng ký model Order
class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'sub_total', 'total', 'status', 'create_time', 'isDelete')
    list_filter = ('status', 'isDelete', 'create_time')
    search_fields = ('user__username', 'status')  # Thay user__name thành user__username

admin.site.register(Order, OrderAdmin)

# Đăng ký model OrderDetail
class OrderDetailAdmin(admin.ModelAdmin):
    list_display = ('order', 'product', 'quantity', 'total', 'discount', 'isDelete')
    list_filter = ('isDelete',)
    search_fields = ('order__id', 'product__name')

admin.site.register(OrderDetail, OrderDetailAdmin)

# Đăng ký model Cart
class CartAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'sub_total', 'total', 'discount', 'is_delete')
    list_filter = ('is_delete',)
    search_fields = ('user__username',)  # Thay user__name thành user__username

admin.site.register(Cart, CartAdmin)

# Đăng ký model CartItem
class CartItemAdmin(admin.ModelAdmin):
    list_display = ('cart', 'product', 'quantity', 'total', 'is_delete')
    list_filter = ('is_delete',)
    search_fields = ('cart__id', 'product__name')

admin.site.register(CartItem, CartItemAdmin)

# Đăng ký model Voucher
class VoucherAdmin(admin.ModelAdmin):
    list_display = ('description', 'discount_percent', 'isDelete')
    list_filter = ('isDelete',)
    search_fields = ('description',)

admin.site.register(Voucher, VoucherAdmin)
