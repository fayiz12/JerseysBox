from django.contrib import admin
from .models import *




class AddressAdmin(admin.ModelAdmin):
    list_display = ('id','user','street_address','city','state','postal_code','country')
     


class OrderAdmin(admin.ModelAdmin):
    list_display = ( 'id','user', 'created_at', 'status', 'total_price','shipping_address','updated_at','payment_mode','sub_total')
    ordering = ('-updated_at',)

class OrderItemAdmin(admin.ModelAdmin):
    list_display = ('id','order','quantity','price','status')

class ReviewAdmin(admin.ModelAdmin):
    list_display = ( 'id','rating','title','description','product','user','created_at')

class ReviewImageAdmin(admin.ModelAdmin):
    list_display = ('id','image','review')



admin.site.register(Review,ReviewAdmin)
admin.site.register(ReviewImage,ReviewImageAdmin)
admin.site.register(Address, AddressAdmin)
admin.site.register(Order, OrderAdmin)
admin.site.register(OrderItem,OrderItemAdmin)