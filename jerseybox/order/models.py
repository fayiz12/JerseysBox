from django.db import models
from users.models import *
from products.models import *
from django_countries.fields import CountryField


class Address(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    name = models.CharField(max_length=100,null=True)  # Add a field for recipient's name
    phone_number = models.CharField(max_length=20,null=True)
    street_address = models.CharField(max_length=255)
    city = models.CharField(max_length=100)
    postal_code = models.CharField(max_length=20)
    state = models.CharField(max_length=100)
    country = CountryField(null=True)
    

class Order(models.Model):
    choices = [('COD', 'Cash On Delivery'), ('Razor Pay', 'Razor Pay')]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True,null=True)
    updated_at = models.DateTimeField(auto_now=True)
    status = models.CharField(max_length=100, default='Pending')
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    # payment = models.ForeignKey('Payment', on_delete=models.SET_NULL, null=True, blank=True)
    shipping_address = models.ForeignKey('Address', on_delete=models.SET_NULL, null=True, blank=True)
    payment_mode=models.CharField(max_length=100,choices=choices,default='Cash On Delivery')
    
    # Add any other fields relevant to your order model  

    def __str__(self):
        return f"Order {self.id} by {self.user}"
    

class OrderItem(models.Model):

    status_choices=[('processing', 'Processing'),
            ('shipped', 'Shipped'), 
            ('delivered', 'Delivered')]
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='order_items')
    product = models.ForeignKey(ProductItem, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=100, choices=status_choices, default='processing')

    def __str__(self):
        return f"OrderItem {self.id} in Order {self.order_id}" 




