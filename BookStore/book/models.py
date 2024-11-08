from django.db import models
from ckeditor.fields import RichTextField
from django.utils import timezone
from pytz import timezone as pytz_timezone
from promotion.models import Promotion


# Product
class Product(models.Model):
    name = models.CharField(max_length=255)
    description = RichTextField(blank=True, null=True)
    image = models.CharField(max_length=255, blank=True, null=True)
    quantity = models.IntegerField(default=0)
    price_origin = models.IntegerField()  
    new_price = models.IntegerField()    
    viewed = models.IntegerField(default=0)
    sub_category = models.ForeignKey('SubCategory', on_delete=models.CASCADE, null=True,related_name='products')
    is_delete = models.BooleanField(default=False)

    publication_year = models.CharField(max_length=4, blank=True, null=True)
    publisher = models.CharField(max_length=255, blank=True, null=True)
    author = models.CharField(max_length=255, blank=True, null=True)
    reprint_edition = models.CharField(max_length=50, blank=True, null=True)
    dimensions = models.CharField(max_length=50, blank=True, null=True)
    cover_type = models.CharField(max_length=50, blank=True, null=True)
    
    promotions = models.ManyToManyField(Promotion, blank=True, related_name="product_promotions")

    def __str__(self):
        return self.name
    
    @property
    def discount_percent(self):
     
        if self.price_origin and self.new_price < self.price_origin:
            return round((1 - (self.new_price / self.price_origin)) * 100, 2)
        return 0

    class Meta:
        db_table = 'product'


#Category
class Category(models.Model):
    name = models.CharField(max_length=255)
    is_delete = models.BooleanField(default=False)

    def __str__(self):
        return self.name
    
    class Meta:
        db_table  = 'category'

#Sub Category
class SubCategory(models.Model):
    name = models.CharField(max_length=255)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, null=True)
    is_delete = models.BooleanField(default=False)

    def __str__(self):
        return self.name
    
    class Meta:
        db_table = 'subcategory'