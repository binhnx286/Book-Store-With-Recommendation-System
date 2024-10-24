from django.db import models

# Product
class Product(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    image = models.CharField(max_length=255, blank=True, null=True)
    quantity = models.IntegerField(default=0)
    price_origin = models.IntegerField()  
    new_price = models.IntegerField()    
    viewed = models.IntegerField(default=0)
    sub_category = models.ForeignKey('SubCategory', on_delete=models.CASCADE, null=True)
    is_delete = models.BooleanField(default=False)

    publication_year = models.CharField(max_length=4, blank=True, null=True)
    publisher = models.CharField(max_length=255, blank=True, null=True)
    author = models.CharField(max_length=255, blank=True, null=True)
    reprint_edition = models.CharField(max_length=50, blank=True, null=True)
    dimensions = models.CharField(max_length=50, blank=True, null=True)
    cover_type = models.CharField(max_length=50, blank=True, null=True)
    

    def __str__(self):
        return self.name
    
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