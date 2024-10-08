# Generated by Django 4.2.15 on 2024-08-21 20:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("rides", "0001_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="Rides",
            fields=[
                ("id", models.IntegerField(primary_key=True, serialize=False)),
                ("name", models.CharField(max_length=255)),
                ("type", models.CharField(max_length=255)),
                ("open_state", models.BooleanField()),
                ("wait_time", models.PositiveSmallIntegerField()),
                ("last_updated", models.DateTimeField()),
            ],
        ),
        migrations.DeleteModel(
            name="Ride_Thrill",
        ),
    ]
