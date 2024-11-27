from django.db import models
from ckeditor.fields import RichTextField
from django.utils import timezone
from pytz import timezone as pytz_timezone
from promotion.models import Promotion
from django.utils.html import strip_tags

# Product
class Product(models.Model):
    name = models.CharField(max_length=255,verbose_name='Tên')
    description = RichTextField(blank=True, null=True,verbose_name='Mô Tả')
    image = models.CharField(max_length=255, blank=True, null=True,verbose_name='Hình ảnh')
    quantity = models.IntegerField(default=0,verbose_name='Tồn kho')
    price_origin = models.IntegerField(verbose_name='Giá gốc')  
    new_price = models.IntegerField(verbose_name='Giá khuyến mãi')    
    viewed = models.IntegerField(default=0,verbose_name='Lượt xem')
    sub_category = models.ForeignKey('SubCategory', on_delete=models.CASCADE, null=True,related_name='products',verbose_name='Danh mục con')
    is_delete = models.BooleanField(default=False,verbose_name='Xóa')

    publication_year = models.CharField(max_length=4, blank=True, null=True,verbose_name='Năm xuất bản')
    publisher = models.CharField(max_length=255, blank=True, null=True,verbose_name='Nhà xuất bản')
    author = models.CharField(max_length=255, blank=True, null=True,verbose_name='Tác giả')
    reprint_edition = models.CharField(max_length=50, blank=True, null=True,verbose_name='Tái bản')
    dimensions = models.CharField(max_length=50, blank=True, null=True,verbose_name='Kích thước')
    cover_type = models.CharField(max_length=50, blank=True, null=True,verbose_name='Loại bìa')
    
    promotions = models.ManyToManyField(Promotion, blank=True, related_name="product_promotions",verbose_name='Các khuyến mãi')

    def __str__(self):
        return self.name
    
    
    @property
    def discount_percent(self):
     
        if self.price_origin and self.new_price < self.price_origin:
            return round((1 - (self.new_price / self.price_origin)) * 100, 2)
        return 0
    @property
    def clean_description(self):
        """Loại bỏ HTML khỏi trường description."""
        return strip_tags(self.description) if self.description else ""
    
    class Meta:
        db_table = 'product'
        verbose_name_plural = 'Sách'


#Category
class Category(models.Model):
    name = models.CharField(max_length=255)
    is_delete = models.BooleanField(default=False)

    def __str__(self):
        return self.name
    
    class Meta:
        db_table  = 'category'
        verbose_name_plural = ' Danh mục'

#Sub Category
class SubCategory(models.Model):
    name = models.CharField(max_length=255)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, null=True)
    is_delete = models.BooleanField(default=False)

    def __str__(self):
        return self.name
    
    class Meta:
        db_table = 'subcategory'
        verbose_name_plural = 'Danh mục con'