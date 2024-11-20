# Generated by Django 5.1.1 on 2024-11-17 02:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("user", "0003_account_image"),
    ]

    operations = [
        migrations.AlterField(
            model_name="account",
            name="image",
            field=models.ImageField(
                blank=True,
                default="avatars/default_avatar.jpg",
                null=True,
                upload_to="profile_images/",
                verbose_name="Ảnh đại diện",
            ),
        ),
    ]
