from django.db import models
from django.forms import ValidationError
import uuid
from categories.models import *


class Product(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    TYPE_CHOICES = [
        ("away", "Away Jersey"),
        ("home", "Home Jersey"),
    ]

    CATEGORY_CHOICES = [
        ("club", "Club"),
        ("country", "Country"),
    ]
    name = models.CharField(max_length=100)
    description = models.TextField()
    is_active = models.BooleanField(default=True)
    is_featured = models.BooleanField(default=False)
    country_id = models.ForeignKey(
        CountryModel, on_delete=models.CASCADE, null=True, blank=True
    )
    club_id = models.ForeignKey(
        Club, on_delete=models.CASCADE, null=True, blank=True)
    type = models.CharField(max_length=10, choices=TYPE_CHOICES)
    category = models.CharField(max_length=10, choices=CATEGORY_CHOICES)

    def save(self, *args, **kwargs):

        if self.category == 'country':
            self.club_id = None
        elif self.category == 'club':
            self.country_id = None
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name


class ProductItem(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    product_id = models.ForeignKey(Product, on_delete=models.CASCADE)
    stock = models.PositiveIntegerField()
    is_active = models.BooleanField(default=True)

    GENDER_CHOICES = [
        ("male", "Male"),
        ("female", "Female"),
        ("kids", "Kids"),
    ]
    gender = models.CharField(max_length=10, choices=GENDER_CHOICES)

    SIZE_CHOICES = [
        ("S", "Small"),
        ("M", "Medium"),
        ("L", "Large"),
    ]

    size = models.CharField(max_length=10, choices=SIZE_CHOICES)

    def __str__(self):
        return f"{self.product_id.name} - {self.get_gender_display()} - {self.get_size_display()}"



class image(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    product_id = models.ForeignKey(ProductItem, on_delete=models.CASCADE)
    image = models.ImageField()
    is_active = models.BooleanField(default=True)
