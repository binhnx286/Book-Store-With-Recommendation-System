# Generated by Django 5.1.1 on 2024-10-24 06:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("cart", "0007_alter_cartitem_total"),
    ]

    operations = [
        migrations.AddField(
            model_name="cart",
            name="is_delete",
            field=models.BooleanField(default=False),
        ),
    ]