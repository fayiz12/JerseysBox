
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

class ProductAdmin(admin.ModelAdmin):
    list_display = ('id','name','price')
     
    class Media:
        js = ('products/product_admin.js',)

    def sales_by_product(self, request):
        product_sales = OrderItem.objects.values('product__product_id__name').annotate(
        total_sales=Sum(models.F('quantity') * models.F('price'))
        )

    # Convert QuerySet to a list of dictionaries
        product_sales_list = list(product_sales)

    # Prepare a list of dictionaries for JSON serialization
        data = [{'product_name': item['product__product_id__name'], 'total_sales': item['total_sales']} for item in product_sales_list]

        context = {
            'product_sales': data,
        }

        return render(request, "admin/sales_by_product.html", context)
    # Add a link to your custom view in the admin list view
    def get_urls(self):
        urls = super().get_urls()
        my_urls = [
            path('sales-by-product/', (self.sales_by_product), name='sales_by_product'),
        ]
        return my_urls + urls

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
