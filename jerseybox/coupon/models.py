from django.db import models
from django.utils import timezone
import uuid

# Create your models here.


class Coupon(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    code = models.CharField(max_length=20, unique=True)
    
    discount_value = models.DecimalField(max_digits=10, decimal_places=2)
    start_date = models.DateField(auto_now_add=True,null=True)
    expiry_date = models.DateField()
    count = models.PositiveIntegerField(default=1)
    is_valid = models.BooleanField(default=True)

    def __str__(self):
        return self.code

    def is_expired(self):
        return self.expiry_date < timezone.now().date()

    def is_usable(self):
        return self.is_valid and not self.is_expired() and self.count > 0