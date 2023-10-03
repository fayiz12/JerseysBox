from django.contrib import admin
from .models import *


class CouponAdmin(admin.ModelAdmin):
    list_display = ('code', 'id','discount_value','start_date','expiry_date','count','is_valid')



admin.site.register(Coupon, CouponAdmin)