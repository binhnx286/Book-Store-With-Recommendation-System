# Generated by Django 5.1.1 on 2024-11-06 14:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("promotion", "0001_initial"),
    ]

    operations = [
        migrations.AlterField(
            model_name="promotion",
            name="promotion_type",
            field=models.CharField(
                choices=[
                    ("product", "Giảm giá cho các sản phẩm"),
                    ("subcategory", "Giảm giá cho danh mục sản phẩm"),
                ],
                default="product",
                max_length=20,
            ),
        ),
    ]