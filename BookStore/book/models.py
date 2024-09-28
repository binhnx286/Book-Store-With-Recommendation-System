from django.db import models

# Product
class Product(models.Model):
    name = models.CharField(max_length=255)
    description = models.CharField(max_length=255, blank=True, null=True)
    image = models.CharField(max_length=255, blank=True, null=True)
    quantity = models.IntegerField(null=True, blank=True)
    price_origin = models.CharField(max_length=255)
    new_price = models.CharField(max_length=255, blank=True, null=True)
    viewed = models.IntegerField(null=True, blank=True)
    sub_category = models.ForeignKey('SubCategory', on_delete=models.SET_NULL, null=True, blank=True)
    brand = models.ForeignKey('Brand', on_delete=models.SET_NULL, null=True, blank=True)
    is_delete = models.BooleanField(default=False)

    def __str__(self):
        return self.name
    
    class Meta:
        db_table = 'product'
    
#Brand 
class Brand(models.Model):
    name = models.CharField(max_length=255)
    logo = models.CharField(max_length=255, blank=True, null=True)
    is_delete = models.BooleanField(default=False)

    def __str__(self):
        return self.name
    
    class Meta:
        db_table = 'brand'
    
    

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
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=True)
    is_delete = models.BooleanField(default=False)

    def __str__(self):
        return self.name
    
    class Meta:
        db_table = 'subcategory'