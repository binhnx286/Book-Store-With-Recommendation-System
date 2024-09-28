from django.db import models
from user.models import Account
from book.models import Product


class Rating(models.Model):
    user = models.ForeignKey(Account,on_delete=models.CASCADE)
    product = models.ForeignKey(Product,on_delete=models.CASCADE)
    rate = models.IntegerField()
    feed_back = models.CharField(max_length=255,blank=True,null=True)
    isDelete = models.BooleanField(default=False)

    def __str__(self):
        return f'Rating for {self.product.name} by {self.user.email}'
    
    class Meta:
        db_table = 'rating'
    