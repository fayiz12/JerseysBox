from django.contrib import admin
from .models import *




class AddressAdmin(admin.ModelAdmin):
    list_display = ('id','user','street_address','city','state','postal_code','country')
     


class OrderAdmin(admin.ModelAdmin):
    list_display = ( 'id','user', 'order_date', 'status', 'total_price','shipping_address','shipping_method')

class OrderItemAdmin(admin.ModelAdmin):
    list_display = ('id','order','quantity','price','status')




admin.site.register(Address, AddressAdmin)
admin.site.register(Order, OrderAdmin)
admin.site.register(OrderItem,OrderItemAdmin)