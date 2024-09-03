# Generated by Django 4.2.15 on 2024-09-02 12:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("rides", "0003_rename_rides_ride"),
    ]

    operations = [
        migrations.CreateModel(
            name="User",
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
                ("email", models.EmailField(max_length=100)),
                ("password", models.CharField(max_length=255)),
            ],
        ),
    ]
