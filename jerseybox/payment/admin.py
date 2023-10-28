from django.contrib import admin
from .models import *
from django.utils import timezone
from django.db.models.functions import TruncDate
from django.db.models import Count
from django.shortcuts import render
import json

class PaymentAdmin(admin.ModelAdmin):
    list_display = ('id','user','transaction_id','amount','status','timestamp')

    def payment_graph(self, request):
        # Get today's date
        today = timezone.now().date()

        # Query successful payments for today
        successful_payments = Payment.objects.filter(
            status='paid',
            timestamp__date=today
        ).annotate(date=TruncDate('timestamp')).values('date').annotate(count=Count('id'))

        # Query failed payments for today
        failed_payments = Payment.objects.filter(
            status='pending',
            timestamp__date=today
        ).annotate(date=TruncDate('timestamp')).values('date').annotate(count=Count('id'))

        # Prepare data for the chart
        chart_data = {
            'labels': [payment['date'].strftime("%a, %d %b %Y") for payment in successful_payments],
            'successful_payments': [payment['count'] for payment in successful_payments],
            'failed_payments': [payment['count'] for payment in failed_payments],
        }

        return render(request, 'admin/payment.html', {'chart_data': json.dumps(chart_data)})

    def get_urls(self):
        from django.urls import path
        urls = super().get_urls()
        custom_urls = [
            path('payment_graph/', (self.payment_graph), name='payment_graph'),
        ]
        return custom_urls + urls

admin.site.register(Payment,PaymentAdmin)

