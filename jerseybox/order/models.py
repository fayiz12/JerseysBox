from django.db import models
from users.models import *
from products.models import *



class Address(models.Model):
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    street_address = models.CharField(max_length=255)
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    postal_code = models.CharField(max_length=20)

class Order(models.Model):
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    order_date = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=100, default='Pending')
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    # payment = models.ForeignKey('Payment', on_delete=models.SET_NULL, null=True, blank=True)
    shipping_address = models.ForeignKey('Address', on_delete=models.SET_NULL, null=True, blank=True)
    shipping_method = models.CharField(max_length=100)  # You can define choices for shipping methods
    # Add any other fields relevant to your order model

class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    product = models.ForeignKey(ProductItem, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=100, default='Processing')