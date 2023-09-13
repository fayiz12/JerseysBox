from django.contrib import admin
from .models import *
from django.utils.safestring import mark_safe

# Register your models here.

class CartAdmin(admin.ModelAdmin):
    list_display = ('id', 'user',)


class CartItemAdmin(admin.ModelAdmin):
    list_display = ('id', 'cart',)


admin.site.register(Cart, CartAdmin)
admin.site.register(CartItem, CartItemAdmin)