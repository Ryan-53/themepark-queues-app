# Generated by Django 4.2.15 on 2024-09-04 12:50

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("rides", "0004_user"),
    ]

    operations = [
        migrations.DeleteModel(
            name="User",
        ),
    ]
