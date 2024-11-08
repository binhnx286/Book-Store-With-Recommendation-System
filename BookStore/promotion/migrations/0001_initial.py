# Generated by Django 5.1.1 on 2024-11-06 09:28

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ("book", "0009_alter_product_description"),
    ]

    operations = [
        migrations.CreateModel(
            name="Promotion",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("name", models.CharField(max_length=255)),
                ("description", models.TextField(blank=True, null=True)),
                ("discount_percent", models.IntegerField()),
                ("start_date", models.DateTimeField()),
                ("end_date", models.DateTimeField()),
                ("is_active", models.BooleanField(default=True)),
                (
                    "promotion_type",
                    models.CharField(
                        choices=[
                            ("product", "Giảm giá cho sản phẩm"),
                            ("subcategory", "Giảm giá cho subcategory"),
                        ],
                        default="product",
                        max_length=20,
                    ),
                ),
                (
                    "products",
                    models.ManyToManyField(
                        blank=True, related_name="promotion_products", to="book.product"
                    ),
                ),
                (
                    "subcategories",
                    models.ManyToManyField(
                        blank=True,
                        related_name="promotion_subcategories",
                        to="book.subcategory",
                    ),
                ),
            ],
            options={
                "db_table": "promotion",
            },
        ),
    ]