from django.db import models
from users.models import *
from products.models import *
from django_countries.fields import CountryField


class Address(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE,related_name='address')
    name = models.CharField(max_length=100,null=True)  # Add a field for recipient's name
    phone_number = models.CharField(max_length=20,null=True)
    street_address = models.CharField(max_length=255)
    city = models.CharField(max_length=100)
    postal_code = models.CharField(max_length=20)
    state = models.CharField(max_length=100)
    country = CountryField(null=True)

    def __str__(self):
        return f" {self.name}  {self.street_address}"
    

class Order(models.Model):
    # choices = [('COD', 'Cash On Delivery'), ('Razor Pay', 'Razor Pay')]
    STATUS_CHOICES = (
        ('Placed', 'Placed'),
        ('Packed', 'Packed'),
        ('Shipped', 'Shipped'),
        ('Delivered', 'Delivered'),
    )

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE,related_name='order')
    created_at = models.DateTimeField(auto_now_add=True,null=True)
    updated_at = models.DateTimeField(auto_now=True)
    status = models.CharField(max_length=100, choices=STATUS_CHOICES,default='Placed')
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    sub_total=models.DecimalField(max_digits=10, decimal_places=2,null=True)
    order_data = models.JSONField(null=True, blank=True)

    # payment = models.ForeignKey('Payment', on_delete=models.SET_NULL, null=True, blank=True)
    shipping_address = models.ForeignKey('Address', on_delete=models.SET_NULL, null=True, blank=True)
    payment_mode=models.CharField(max_length=100,null=True)
    coupon_discount=models.IntegerField(default=0)
    
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
    item_data = models.JSONField(null=True, blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=100, choices=status_choices, default='processing')

    def __str__(self):
        return f"OrderItem {self.id} in Order {self.order_id}" 




class Review(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    rating = models.IntegerField()
    title = models.CharField(max_length=200)
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True,null=True)
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='reviews')
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name='reviews')

class ReviewImage(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    image = models.ImageField(upload_to='review_images/', null=True, blank=True)
    review = models.ForeignKey(Review, on_delete=models.CASCADE, related_name='review_images')