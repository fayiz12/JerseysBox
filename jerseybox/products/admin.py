
# Register your models here.
from django.contrib import admin
from .models import *
from django.utils.safestring import mark_safe
from django.contrib import admin
from django.contrib.admin.views.decorators import staff_member_required
from django.shortcuts import render
from django.db.models import Sum
from django.urls import path 
from order.models import *
from django.core import serializers
from django.http import JsonResponse
from django.db.models import F
import locale


class ProductAdmin(admin.ModelAdmin):
    list_display = ('id','name','price')
     
    class Media:
        js = ('products/product_admin.js',)
        

class ProductItemAdmin(admin.ModelAdmin):
    list_display = ( 'id','product_id', 'stock', 'is_active', 'size')

class ImageAdmin(admin.ModelAdmin):
    list_display = ('product','display_image')


    def display_image(self, obj):
        return mark_safe(f'<img src="{obj.image.url}" alt="jersey image" style="max-width: 100px; max-height: 100px;">')
    
    display_image.short_description = 'Image'





admin.site.register(Product, ProductAdmin)
admin.site.register(ProductItem, ProductItemAdmin)
admin.site.register(Image,ImageAdmin)
