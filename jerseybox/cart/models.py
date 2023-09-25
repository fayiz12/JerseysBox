from django.db import models
from users.models import *
import uuid
from products.models import *

class Cart(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.OneToOneField(UserProfile, on_delete=models.CASCADE,null=True,blank=True)
    completed = models.BooleanField(default=False)
    session_id = models.CharField(max_length=100, null=True, blank=True)
    total = models.DecimalField(max_digits=10, decimal_places=2, default=0)  # Add this field
    
    def update_total(self):
        cart_items = self.cart.all()
        total = sum(cart_item.total for cart_item in cart_items)
        self.total = total
        self.save()

    def __str__(self):
        return f"Cart for {self.user.username}"
    

class CartItem(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE,null=True, blank=True,related_name='cart')
    product_item = models.ForeignKey(ProductItem, on_delete=models.CASCADE,related_name='cart_item')
    quantity = models.PositiveIntegerField(default=1)
    status = models.CharField(max_length=20, default='active')
    total = models.DecimalField(max_digits=10, decimal_places=2, default=0) 
    def save(self, *args, **kwargs):
        # Calculate the total based on the product's price and quantity
        if self.product_item:
            self.total = self.product_item.product_id.price * self.quantity
        else:
            self.total = 0  # Handle the case where the product_item is not set

        super(CartItem, self).save(*args, **kwargs)

        # Update the Cart's total when the CartItem is saved
        self.cart.update_total()

    def delete(self, *args, **kwargs):
        super(CartItem, self).delete(*args, **kwargs)

        # Update the Cart's total when a CartItem is deleted
        self.cart.update_total()

    def __str__(self):
        return f"Cart item for {self.product_item}"

    
    


