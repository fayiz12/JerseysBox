# Generated by Django 4.2.4 on 2023-09-24 08:03

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):
    initial = True

    dependencies = [
        ("products", "0017_alter_product_unique_together"),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ("order", "0002_remove_order_shipping_address_remove_order_user_and_more"),
    ]

    operations = [
        migrations.CreateModel(
            name="Address",
            fields=[
                (
                    "id",
                    models.UUIDField(
                        default=uuid.uuid4,
                        editable=False,
                        primary_key=True,
                        serialize=False,
                    ),
                ),
                ("street_address", models.CharField(max_length=255)),
                ("city", models.CharField(max_length=100)),
                ("state", models.CharField(max_length=100)),
                ("postal_code", models.CharField(max_length=20)),
                (
                    "user",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="Order",
            fields=[
                (
                    "id",
                    models.UUIDField(
                        default=uuid.uuid4,
                        editable=False,
                        primary_key=True,
                        serialize=False,
                    ),
                ),
                ("order_date", models.DateTimeField(auto_now_add=True)),
                ("status", models.CharField(default="Pending", max_length=100)),
                ("total_price", models.DecimalField(decimal_places=2, max_digits=10)),
                ("shipping_method", models.CharField(max_length=100)),
                (
                    "shipping_address",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        to="order.address",
                    ),
                ),
                (
                    "user",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="OrderItem",
            fields=[
                (
                    "id",
                    models.UUIDField(
                        default=uuid.uuid4,
                        editable=False,
                        primary_key=True,
                        serialize=False,
                    ),
                ),
                ("quantity", models.PositiveIntegerField()),
                ("price", models.DecimalField(decimal_places=2, max_digits=10)),
                ("status", models.CharField(default="Processing", max_length=100)),
                (
                    "order",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE, to="order.order"
                    ),
                ),
                (
                    "product",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="products.productitem",
                    ),
                ),
            ],
        ),
    ]