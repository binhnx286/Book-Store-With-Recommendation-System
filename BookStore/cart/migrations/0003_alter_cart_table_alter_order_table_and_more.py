# Generated by Django 5.1.1 on 2024-09-29 09:15

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("cart", "0002_voucher"),
    ]

    operations = [
        migrations.AlterModelTable(
            name="cart",
            table="cart",
        ),
        migrations.AlterModelTable(
            name="order",
            table="order",
        ),
        migrations.AlterModelTable(
            name="orderdetail",
            table="orderdetail",
        ),
        migrations.AlterModelTable(
            name="voucher",
            table="voucher",
        ),
    ]
