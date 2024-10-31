from django.db import models
from user.models import Account
from book.models import Product

class Order(models.Model):
    discount = models.IntegerField(null=True, blank=True)
    sub_total = models.IntegerField()
    total = models.IntegerField()
    shipping = models.IntegerField(default=0)
    create_time = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=255, default='Pending')
    user = models.ForeignKey(Account, on_delete=models.CASCADE)
    isDelete = models.BooleanField(default=False)

    def __str__(self):
        return f"Order {self.id} - {self.user.name}"
    
    class Meta:
        db_table = 'order'

class OrderDetail(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField()
    total = models.IntegerField()
    discount = models.IntegerField(null=True, blank=True)
    isDelete = models.BooleanField(default=False)

    def __str__(self):
        return f"OrderDetail {self.order.id} - {self.product.name}"
    
    
    class Meta:
        db_table = 'orderdetail'

class Cart(models.Model):
    discount = models.IntegerField(null=True, blank=True)
    sub_total = models.IntegerField(null=True, blank=True)
    total = models.IntegerField(default=0)
    is_delete = models.BooleanField(default=False)
    user = models.ForeignKey(Account, on_delete=models.CASCADE)

    def calculate_totals(self):
        self.sub_total = sum(item.quantity * item.price() for item in self.cart_items.filter(is_delete=False))
        self.total = self.sub_total - (self.discount or 0)
        self.save()

    def __str__(self):
        return f"Cart {self.id} - {self.user.name}"

    class Meta:
        db_table = 'cart'

class CartItem(models.Model):
    cart = models.ForeignKey(Cart, related_name='cart_items', on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=0)
    total = models.IntegerField( default=0)  
    is_delete = models.BooleanField(default=False)
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

class Voucher(models.Model):
    discount_percent = models.IntegerField()
    description = models.CharField(max_length=255, blank=True, null=True)
    isDelete = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.description} - {self.discount_percent}% discount"
    
    
    class Meta:
        db_table = 'voucher'
