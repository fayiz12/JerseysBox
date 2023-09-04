
# Register your models here.
from django.contrib import admin
from .models import *
from django.utils.safestring import mark_safe



class ProductAdmin(admin.ModelAdmin):
    list_display = ('id','name',)


class ProductItemAdmin(admin.ModelAdmin):
    list_display = ( 'id','product_id','actual_price','selling_price','discount_percent', 'stock', 'is_active', 'gender', 'size')

class ImageAdmin(admin.ModelAdmin):
    list_display = ('product_id','display_image')


    def display_image(self, obj):
        return mark_safe(f'<img src="{obj.image.url}" alt="jersey image" style="max-width: 100px; max-height: 100px;">')
    
    display_image.short_description = 'Image'

admin.site.register(Product, ProductAdmin)
admin.site.register(ProductItem, ProductItemAdmin)
admin.site.register(image,ImageAdmin)
