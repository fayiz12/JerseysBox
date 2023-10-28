from django.contrib import admin
from .models import *
from .forms import *
from django.urls import path
from django.shortcuts import render
from django.db.models.functions import TruncDay, TruncMonth
from django.db.models import F, Sum

class AddressAdmin(admin.ModelAdmin):
    list_display = ('id','user','street_address','city','state','postal_code','country')
     


class OrderAdmin(admin.ModelAdmin):
    list_display = ( 'id','user', 'created_at', 'status', 'total_price','shipping_address','updated_at','payment_mode','sub_total')
    ordering = ('-updated_at',)
    form = OrderAdminForm

    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path('sales_chart/', self.sales_chart_view, name='sales-chart'),
        ]
        return custom_urls + urls

    def sales_chart_view(self, request):
        interval = request.GET.get('interval', 'daily')
        user=UserProfile.objects.count()
        # Query the data for the chart
        # Depending on the chosen interval (daily or monthly), use TruncDay or TruncMonth
        if interval == 'daily':
            sales_data = (
                Order.objects
                .annotate(date=TruncDay('created_at'))
                .values('date')
                .annotate(total_revenue=Sum('total_price'))
                .order_by('date')
            )
        elif interval == 'monthly':
            sales_data = (
                Order.objects
                .annotate(month=TruncMonth('created_at'))
                .values('month')
                .annotate(total_revenue=Sum('total_price'))
                .order_by('month')
            )

        labels = [str(item['date'].strftime('%b %d, %Y')) if interval == 'daily' else str(item['month'].strftime('%b %Y')) for item in sales_data]
        revenue_data = [float(item['total_revenue']) for item in sales_data]

        chart_data = {
            'labels': labels,
            'revenue_data': revenue_data,
        }

        return render(request, 'admin/index.html', {'chart_data': chart_data, 'interval': interval ,'user_count':user})

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


