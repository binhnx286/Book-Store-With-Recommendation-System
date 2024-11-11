from django.db import models
from django.utils import timezone
from django.core.exceptions import ValidationError
from ckeditor_uploader.fields import RichTextUploadingField


class Promotion(models.Model):
    PROMOTION_TYPE_CHOICES = [
        ('product', 'Giảm giá cho các sản phẩm'),
        ('subcategory', 'Giảm giá cho danh mục sản phẩm')
    ]

    name = models.CharField(max_length=255)
    short_description = models.CharField(max_length=255, blank=True, null=True)
    description = RichTextUploadingField(blank=True, null=True)
    discount_percent = models.IntegerField()  # Phần trăm giảm giá
    start_date = models.DateTimeField()      # Ngày bắt đầu
    end_date = models.DateTimeField()        # Ngày kết thúc
    is_active = models.BooleanField(default=True)  # Trạng thái chiến dịch

    promotion_type = models.CharField(max_length=20, choices=PROMOTION_TYPE_CHOICES, default='product')
    image = models.ImageField(upload_to='promotions/', blank=True, null=True)  
    
    subcategories = models.ManyToManyField('book.SubCategory', blank=True, related_name="promotion_subcategories")
    products = models.ManyToManyField('book.Product', blank=True, related_name="promotion_products")

    def __str__(self):
        return f"{self.pk} - {self.name} - {self.discount_percent}% off"

    def is_active_promotion(self):
        """Kiểm tra chiến dịch có đang hoạt động hay không"""
        return self.is_active and self.start_date <= timezone.now() <= self.end_date

    
    def update_new_price(self):
        """Cập nhật giá cho các sản phẩm thuộc chương trình khuyến mãi"""
       
        
        if self.is_active and self.start_date <= timezone.now() <= self.end_date:
            print(f"Promotion {self.name} is active.")
            for subcategory in self.subcategories.all():
                print(f"Products in Subcategory {subcategory.name}:")
                for product in subcategory.products.all():
                    # print(f"- {product.name} (Price: {product.price_origin})")
                    new_price = int(product.price_origin * (1 - self.discount_percent / 100))
                    if product.new_price != new_price:
                        product.new_price = new_price
                        product.save() 
            for product in self.products.all():
                # print(f"Original Price for {product.name}: {product.price_origin}")
                # print(f"New Price for {product.name}: {product.new_price}")
                new_price = int(product.price_origin * (1 - self.discount_percent / 100))
            
                # In ra giá mới
                print(f"New Price Disc for {product.name}: {new_price}")
                if product.new_price != new_price:
                    product.new_price = new_price
                    product.save()  # Lưu thay đổi vào cơ sở dữ liệu
        else:
            print(f"Promotion {self.name} is not active or expired.")
            for subcategory in self.subcategories.all():  # Lặp qua các SubCategory
                for product in subcategory.products.all():  # Lặp qua các sản phẩm trong SubCategory
                    if product.new_price != product.price_origin:
                        product.new_price = product.price_origin
                        product.save()  # Lưu lại giá gốc
                        print(f"Restored original price for {product.name}: {product.price_origin}")
            for product in self.products.all():
                if product.new_price != product.price_origin:
                    product.new_price = product.price_origin
                    product.save()  # Lưu lại giá gốc
                    print(f"Restored original price for {product.name}: {product.price_origin}")

    def save(self, *args, **kwargs):
        
        super().save(*args, **kwargs)

    class Meta:
        db_table = 'promotion'
