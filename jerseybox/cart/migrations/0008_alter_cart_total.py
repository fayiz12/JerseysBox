# Generated by Django 4.2.4 on 2023-09-30 07:20

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("cart", "0007_cart_total"),
    ]

    operations = [
        migrations.AlterField(
            model_name="cart",
            name="total",
            field=models.IntegerField(default=0),
        ),
    ]