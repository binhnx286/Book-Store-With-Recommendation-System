from celery import shared_task
from django.utils import timezone
from .models import Promotion

@shared_task
def update_expired_promotions_price():
    # Lấy tất cả các promotion đã hết hạn
    promotions = Promotion.objects.filter(end_date__lt=timezone.now())

    # Cập nhật giá mới cho mỗi promotion đã hết hạn
    for promotion in promotions:
        promotion.update_new_price()
        promotion.is_active = False
        promotion.save() 
        print(f"Đã cập nhật giá mới cho khuyến mãi hết hạn: {promotion.name}")
