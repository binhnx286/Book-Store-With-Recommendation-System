# Generated by Django 5.1.1 on 2024-09-16 06:45

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Role",
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
            ],
            options={
                "db_table": "role",
            },
        ),
        migrations.CreateModel(
            name="Account",
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
                ("password", models.CharField(max_length=255)),
                ("phone", models.CharField(blank=True, max_length=255, null=True)),
                ("email", models.EmailField(max_length=254, unique=True)),
                ("address", models.CharField(blank=True, max_length=255, null=True)),
                ("status", models.BooleanField(default=True)),
                (
                    "role",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="accounts",
                        to="user.role",
                    ),
                ),
            ],
            options={
                "db_table": "account",
            },
        ),
    ]
