# Generated by Django 5.1.1 on 2024-10-23 08:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("book", "0007_alter_product_new_price_alter_product_price_origin"),
    ]

    operations = [
        migrations.AlterField(
            model_name="product",
            name="new_price",
            field=models.IntegerField(),
        ),
        migrations.AlterField(
            model_name="product",
            name="price_origin",
            field=models.IntegerField(),
        ),
    ]