
# Register your models here.
from django.contrib import admin
from .models import *






class ProductAdmin(admin.ModelAdmin):
    list_display = ('name',)


class ProductItemAdmin(admin.ModelAdmin):
    list_display=('id',)

admin.site.register(Product, ProductAdmin)
admin.site.register(ProductItem, ProductItemAdmin)
admin.site.register(image)
