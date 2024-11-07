from django.db.models.signals import post_save,m2m_changed
from django.dispatch import receiver
from django.utils import timezone
from .models import Promotion

@receiver(post_save, sender=Promotion)
def update_product_prices_on_promotion_save(sender, instance, **kwargs):
    """Cập nhật giá cho các sản phẩm khi chiến dịch khuyến mãi thay đổi hoặc mới được lưu"""
    # Chỉ cập nhật giá khi chương trình khuyến mãi đang hoạt động
    today = timezone.now()
    if instance.is_active and instance.start_date <= today <= instance.end_date:
        print(f"Updating prices for products in promotion: {instance.name}")
        instance.update_new_price()  # Gọi hàm update_new_price từ Promotion
    else:
        print(f"Promotion {instance.name} is not active or expired.")
        instance.update_new_price()  # Cập nhật giá sản phẩm nếu chương trình không còn hiệu lực
@receiver(m2m_changed, sender=Promotion.products.through)
def update_prices_on_product_add(sender, instance, action, reverse, model, pk_set, **kwargs):
    """Cập nhật giá khi sản phẩm được thêm vào chiến dịch khuyến mãi"""
    if action == 'post_add':
        instance.update_new_price()  # Gọi hàm cập nhật giá cho sản phẩm
    elif action == 'post_remove':
        for product_id in pk_set:
            product = model.objects.get(id=product_id)
            if product.new_price != product.price_origin:
                product.new_price = product.price_origin
                product.save()  # Lưu lại giá gốc
            print(f"Restored original price for {product.name}: {product.price_origin}")
@receiver(m2m_changed, sender=Promotion.subcategories.through)
def update_prices_on_subcategory_add(sender, instance, action, reverse, model, pk_set, **kwargs):
    """Cập nhật giá khi subcategory được thêm vào hoặc xóa khỏi chiến dịch khuyến mãi"""
    
    if action == 'post_add':
        instance.update_new_price()  
    elif action == 'post_remove':
        # Khi subcategory bị xóa khỏi chiến dịch khuyến mãi
        print(f"Subcategories removed from promotion {instance.name}: {instance.subcategories.all()}")
        for subcategory_id in pk_set:
            subcategory = model.objects.get(id=subcategory_id)
            print(f"Restoring original price for products in Subcategory {subcategory.name}:")
            for product in subcategory.products.all():  # Lặp qua các sản phẩm trong SubCategory
                    if product.new_price != product.price_origin:
                        product.new_price = product.price_origin
                        product.save()  # Lưu lại giá gốc
                    print(f"Restored original price for {product.name}: {product.price_origin}")

        