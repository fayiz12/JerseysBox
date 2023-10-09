from django.db import models
from django.core.validators import MinValueValidator
from django.forms import ValidationError
import uuid
from categories.models import CountryModel, Club


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
    YEAR_CHOICES = [
        ("23-24", "2023-2024"),
        ("22-23", "2022-2023"),
        ("21-22", "2021-2022"),
        ("20-21", "2020-2021"),
        ("19-20", "2019-2020"),
    ]

    name = models.CharField(max_length=100)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2, null=True, validators=[MinValueValidator(0.01)])
    is_active = models.BooleanField(default=True)
    is_featured = models.BooleanField(default=False)
    category = models.CharField(max_length=10, choices=CATEGORY_CHOICES)
    country_id = models.ForeignKey(
        CountryModel, on_delete=models.CASCADE, null=True, blank=True
    )
    club_id = models.ForeignKey(
        Club, on_delete=models.CASCADE, null=True, blank=True, related_name='products'
    )
    type = models.CharField(max_length=10, choices=TYPE_CHOICES)

    GENDER_CHOICES = [
        ("male", "Male"),
        ("female", "Female"),
        ("kids", "Kids"),
    ]
    gender = models.CharField(max_length=10, choices=GENDER_CHOICES)
    year = models.CharField(max_length=5, null=True, choices=YEAR_CHOICES)

    class Meta:
        unique_together = (
            ('country_id', 'type', 'year', 'gender'),
            ('club_id', 'type', 'year', 'gender')
        )

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
    product_id = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='productitem')
    stock = models.PositiveIntegerField()
    is_active = models.BooleanField(default=True)

    SIZE_CHOICES = [
        ("S", "Small"),
        ("M", "Medium"),
        ("L", "Large"),
    ]

    size = models.CharField(max_length=10, choices=SIZE_CHOICES)

    def __str__(self):
        return f"{self.product_id.name} - {self.get_size_display()}"

class Image(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='image')
    image = models.ImageField()
    is_active = models.BooleanField(default=True)
    is_featured = models.BooleanField(default=False)



