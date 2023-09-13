from django.db import models
from users.models import *
import uuid
from products.models import *

class Cart(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.OneToOneField(UserProfile, on_delete=models.CASCADE,null=True,blank=True)
    completed = models.BooleanField(default=False)
    session_id = models.CharField(max_length=100, null=True, blank=True)
    
    
    def __str__(self):
        return f"Cart for {self.user.username}"
    

class CartItem(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE,null=True, blank=True)
    product_item = models.ForeignKey(ProductItem, on_delete=models.CASCADE,related_name='cart_item')
    quantity = models.PositiveIntegerField(default=1)
    status = models.CharField(max_length=20, default='active')


    def __str__(self):
        return f"Cart item for {self.product_item}"
    


