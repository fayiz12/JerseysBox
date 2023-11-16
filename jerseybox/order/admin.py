from django.contrib import admin
from .models import *
from .forms import *
from django.urls import path
from django.shortcuts import render
from django.db.models.functions import TruncDay, TruncMonth
from django.db.models import F, Sum
from django.db.models import Count
from payment.models import *
from django.db.models.functions import Extract


class AddressAdmin(admin.ModelAdmin):
    list_display = ('id','user','street_address','city','state','postal_code','country','created_at')
     


class OrderAdmin(admin.ModelAdmin):
    list_display = ( 'id','user', 'created_at', 'status', 'total_price','shipping_address','updated_at','payment_mode','coupon_discount','sub_total')
    ordering = ('-updated_at',)
    form = OrderAdminForm


class OrderItemAdmin(admin.ModelAdmin):
    list_display = ('id','order','quantity','price','status')

class ReviewAdmin(admin.ModelAdmin):
    list_display = ( 'id','rating','title','description','product','user','created_at')

class ReviewImageAdmin(admin.ModelAdmin):
    list_display = ('id','image','review')

class MyCustomAdminView(admin.AdminSite):
    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path('my_custom_page/', self.admin_view(self.my_custom_view), name='my_custom_page'),
        ]
        return custom_urls + urls

    def my_custom_view(self, request):
        # Your custom view logic goes here
        custom_context = {'custom_variable': 'This is a custom variable.'}
        return render(request, 'admin/index.html', context=custom_context)

admin_site = MyCustomAdminView(name='myadmin')

admin.site.register(Review,ReviewAdmin)
admin.site.register(ReviewImage,ReviewImageAdmin)
admin.site.register(Address, AddressAdmin)
admin.site.register(Order, OrderAdmin)
admin.site.register(OrderItem,OrderItemAdmin)


