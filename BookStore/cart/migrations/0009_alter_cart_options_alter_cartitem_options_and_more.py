# Generated by Django 5.1.1 on 2024-11-13 07:18

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('book', '0012_alter_category_options_alter_product_options_and_more'),
        ('cart', '0008_cart_is_delete'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='cart',
            options={'verbose_name_plural': 'Giỏ hàng'},
        ),
        migrations.AlterModelOptions(
            name='cartitem',
            options={'verbose_name_plural': 'Chi tiết giỏ hàng'},
        ),
        migrations.AlterModelOptions(
            name='order',
            options={'verbose_name_plural': 'Đơn đặt hàng'},
        ),
        migrations.AlterModelOptions(
            name='orderdetail',
            options={'verbose_name_plural': 'Chi tiết đơn hàng'},
        ),
        migrations.AlterModelOptions(
            name='voucher',
            options={'verbose_name_plural': 'Mã khuyến mãi'},
        ),
        migrations.AlterField(
            model_name='cart',
            name='discount',
            field=models.IntegerField(blank=True, null=True, verbose_name='Giảm giá'),
        ),
        migrations.AlterField(
            model_name='cart',
            name='is_delete',
            field=models.BooleanField(default=False, verbose_name='Đã xóa'),
        ),
        migrations.AlterField(
            model_name='cart',
            name='sub_total',
            field=models.IntegerField(blank=True, null=True, verbose_name='Tổng phụ'),
        ),
        migrations.AlterField(
            model_name='cart',
            name='total',
            field=models.IntegerField(default=0, verbose_name='Tổng cộng'),
        ),
        migrations.AlterField(
            model_name='cart',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='Người dùng'),
        ),
        migrations.AlterField(
            model_name='cartitem',
            name='cart',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='cart_items', to='cart.cart', verbose_name='Giỏ hàng'),
        ),
        migrations.AlterField(
            model_name='cartitem',
            name='is_delete',
            field=models.BooleanField(default=False, verbose_name='Đã xóa'),
        ),
        migrations.AlterField(
            model_name='cartitem',
            name='product',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='book.product', verbose_name='Sản phẩm'),
        ),
        migrations.AlterField(
            model_name='cartitem',
            name='quantity',
            field=models.IntegerField(default=0, verbose_name='Số lượng'),
        ),
        migrations.AlterField(
            model_name='cartitem',
            name='total',
            field=models.IntegerField(default=0, verbose_name='Tổng cộng'),
        ),
        migrations.AlterField(
            model_name='order',
            name='create_time',
            field=models.DateTimeField(auto_now_add=True, verbose_name='Thời gian tạo'),
        ),
        migrations.AlterField(
            model_name='order',
            name='discount',
            field=models.IntegerField(blank=True, null=True, verbose_name='Giảm giá'),
        ),
        migrations.AlterField(
            model_name='order',
            name='isDelete',
            field=models.BooleanField(default=False, verbose_name='Đã xóa'),
        ),
        migrations.AlterField(
            model_name='order',
            name='shipping',
            field=models.IntegerField(default=0, verbose_name='Phí vận chuyển'),
        ),
        migrations.AlterField(
            model_name='order',
            name='status',
            field=models.CharField(default='Pending', max_length=255, verbose_name='Trạng thái'),
        ),
        migrations.AlterField(
            model_name='order',
            name='sub_total',
            field=models.IntegerField(verbose_name='Tổng tạm tính'),
        ),
        migrations.AlterField(
            model_name='order',
            name='total',
            field=models.IntegerField(verbose_name='Tổng cộng'),
        ),
        migrations.AlterField(
            model_name='order',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='Người mua'),
        ),
        migrations.AlterField(
            model_name='orderdetail',
            name='discount',
            field=models.IntegerField(blank=True, null=True, verbose_name='Giảm giá'),
        ),
        migrations.AlterField(
            model_name='orderdetail',
            name='isDelete',
            field=models.BooleanField(default=False, verbose_name='Đã xóa'),
        ),
        migrations.AlterField(
            model_name='orderdetail',
            name='order',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='cart.order', verbose_name='Mã đơn'),
        ),
        migrations.AlterField(
            model_name='orderdetail',
            name='product',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='book.product', verbose_name='Sản phẩm'),
        ),
        migrations.AlterField(
            model_name='orderdetail',
            name='quantity',
            field=models.IntegerField(verbose_name='Số lượng'),
        ),
        migrations.AlterField(
            model_name='orderdetail',
            name='total',
            field=models.IntegerField(verbose_name='Tổng cộng'),
        ),
    ]
