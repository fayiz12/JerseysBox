# Generated by Django 4.2.4 on 2023-08-21 13:41

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("categories", "0005_countrymodel_flag_image_path"),
    ]

    operations = [
        migrations.AlterField(
            model_name="countrymodel",
            name="flag_image_path",
            field=models.CharField(default=None, max_length=100),
        ),
    ]
