from django.db import models
from user.models import Account
from book.models import Product

class Order(models.Model):
    discount = models.IntegerField(null=True, blank=True, verbose_name='Giảm giá')
    sub_total = models.IntegerField(verbose_name='Tổng tạm tính')
    total = models.IntegerField(verbose_name='Tổng cộng')
    shipping = models.IntegerField(default=0, verbose_name='Phí vận chuyển')
    create_time = models.DateTimeField(auto_now_add=True, verbose_name='Thời gian tạo')
    status = models.CharField(max_length=255, default='Pending', verbose_name='Trạng thái')
    user = models.ForeignKey(Account, on_delete=models.CASCADE,verbose_name='Người mua')
    isDelete = models.BooleanField(default=False, verbose_name='Đã xóa')

    def __str__(self):
        return f"Order {self.id} - {self.user.username}"
    
    class Meta:
        db_table = 'order'
        verbose_name_plural = 'Đơn đặt hàng'

class OrderDetail(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE,verbose_name='Mã đơn')
    product = models.ForeignKey(Product, on_delete=models.CASCADE,verbose_name='Sản phẩm')
    quantity = models.IntegerField(verbose_name='Số lượng')
    total = models.IntegerField(verbose_name='Tổng cộng')
    discount = models.IntegerField(null=True, blank=True, verbose_name='Giảm giá')
    isDelete = models.BooleanField(default=False, verbose_name='Đã xóa')

    def __str__(self):
        return f"OrderDetail {self.order.id} - {self.product.name}"
    
    
    class Meta:
        db_table = 'orderdetail'
        verbose_name_plural = 'Chi tiết đơn hàng'

class Cart(models.Model):
    discount = models.IntegerField(null=True, blank=True, verbose_name='Giảm giá')
    sub_total = models.IntegerField(null=True, blank=True, verbose_name='Tổng phụ')
    total = models.IntegerField(default=0, verbose_name='Tổng cộng')
    is_delete = models.BooleanField(default=False, verbose_name='Đã xóa')
    user = models.ForeignKey(Account, on_delete=models.CASCADE,verbose_name='Người dùng')

    def calculate_totals(self):
        self.sub_total = sum(item.quantity * item.price() for item in self.cart_items.filter(is_delete=False))
        self.total = self.sub_total - (self.discount or 0)
        self.save()

    def __str__(self):
        return f"Cart- {self.user.username}"

    class Meta:
        db_table = 'cart'
        verbose_name_plural = 'Giỏ hàng'

class CartItem(models.Model):
    cart = models.ForeignKey(Cart, related_name='cart_items', on_delete=models.CASCADE, verbose_name='Giỏ hàng')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name='Sản phẩm')
    quantity = models.IntegerField(default=0, verbose_name='Số lượng')
    total = models.IntegerField(default=0, verbose_name='Tổng cộng')
    is_delete = models.BooleanField(default=False, verbose_name='Đã xóa')
    def price(self):
        return self.product.new_price  

    def save(self, *args, **kwargs):
        self.total = self.price() * self.quantity  # Tính tổng ngay trong phương thức save
        super().save(*args, **kwargs)
        self.cart.calculate_totals()  # Cập nhật tổng khi lưu CartItem

    def __str__(self):
        return f"CartItem {self.cart.id} - {self.product.name}"

    class Meta:
        db_table = 'cart_item'
        verbose_name_plural = 'Chi tiết giỏ hàng'

class Voucher(models.Model):
    discount_percent = models.IntegerField()
    description = models.CharField(max_length=255, blank=True, null=True)
    isDelete = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.description} - {self.discount_percent}% discount"
    
    
    class Meta:
        db_table = 'voucher'
        verbose_name_plural = 'Mã khuyến mãi'
