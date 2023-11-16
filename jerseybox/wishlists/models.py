from django.db import models
from users.models import *
import uuid
from products.models import *




class WishlistModel(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE, null=True, blank=True)
    product = models.ManyToManyField(Product, related_name='wishlist_items') 

    def __str__(self):
        return f"Wishlist for {self.user.username}"