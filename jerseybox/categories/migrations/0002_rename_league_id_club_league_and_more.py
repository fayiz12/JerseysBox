# Generated by Django 4.2.4 on 2023-08-20 04:18

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("categories", "0001_initial"),
    ]

    operations = [
        migrations.RenameField(
            model_name="club",
            old_name="league_id",
            new_name="league",
        ),
        migrations.RenameField(
            model_name="countrymodel",
            old_name="continent_id",
            new_name="continent",
        ),
        migrations.RenameField(
            model_name="league",
            old_name="country_id",
            new_name="country",
        ),
    ]
