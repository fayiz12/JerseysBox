from django.db import models
from django.forms import ValidationError
import uuid
from categories.models import *
from django.core.validators import MinValueValidator
from users.models import *

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
        Club, on_delete=models.CASCADE, null=True, blank=True,related_name='products')
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
    product_id = models.ForeignKey(Product, on_delete=models.CASCADE,related_name='productitem')
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
    actual_price = models.DecimalField(max_digits=10, decimal_places=2,null=True, validators=[MinValueValidator(0.01)])
    selling_price = models.DecimalField(max_digits=10, decimal_places=2,null=True, validators=[MinValueValidator(0.01)])
    
    discount_percent = models.IntegerField( default=0,null=True, validators=[MinValueValidator(0)])

    def __str__(self):
        return f"{self.product_id.name} - {self.get_gender_display()} - {self.get_size_display()}"

    def clean(self):
        if self.selling_price > self.actual_price:
            raise ValidationError("Selling price must be lesser than or equal to the actual price")

    def save(self, *args, **kwargs):
        if self.actual_price > 0:
            self.discount_percent = round(((self.actual_price - self.selling_price) / self.actual_price) * 100)
        else:
            self.discount_percent = 0
        super().save(*args, **kwargs)


class image(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    product_id = models.ForeignKey(ProductItem, on_delete=models.CASCADE,related_name='image')
    image = models.ImageField()
    is_active = models.BooleanField(default=True)
    is_featured = models.BooleanField(default=False)



class Cart(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.OneToOneField(UserProfile, on_delete=models.CASCADE)
    total_price = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    total_quantity = models.PositiveIntegerField(default=0)
    status = models.CharField(max_length=20, default='active')

    def __str__(self):
        return f"Cart for {self.user.username}"
    

class CartItem(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
    product_item = models.ForeignKey(ProductItem, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"Cart item for {self.product_item}"