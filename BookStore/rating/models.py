from django.db import models
from user.models import Account
from book.models import Product
from django.core.exceptions import ValidationError


class Rating(models.Model):
    user = models.ForeignKey(Account, on_delete=models.CASCADE, verbose_name='Người đánh giá')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name='Sách')
    rate = models.IntegerField(verbose_name='Xếp hạng')
    feed_back = models.CharField(max_length=255, blank=True, null=True, verbose_name='Nhận xét')
    isDelete = models.BooleanField(default=False, verbose_name='Xóa')
    is_disabled = models.BooleanField(default=False, verbose_name='Tắt phản hồi')  # Trường kiểm soát trạng thái

    def __str__(self):
        return f'Đánh giá cho {self.product.name} bởi {self.user.email}'

    class Meta:
        db_table = 'rating'
        verbose_name_plural = 'Đánh giá'

class RatingResponse(models.Model):
    rating = models.ForeignKey(Rating, on_delete=models.CASCADE, related_name='responses', verbose_name='Đánh giá')
    user = models.ForeignKey(Account, on_delete=models.CASCADE, verbose_name='Người phản hồi')
    response_text = models.TextField(verbose_name='Phản hồi')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Thời gian tạo')

    def __str__(self):
        return f'Phản hồi từ {self.user.email} cho đánh giá {self.rating.id}'

    class Meta:
        db_table = 'rating_response'
        verbose_name_plural = 'Phản hồi cho đánh giá'
        ordering = ['created_at']

    def clean(self):
        if self.rating.is_disabled:
            raise ValidationError("Không thể phản hồi cho đánh giá này vì nó đã bị tắt.")

        
    