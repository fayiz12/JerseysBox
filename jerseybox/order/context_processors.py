from .models import *
from django.db.models.functions import TruncDay, TruncMonth
from django.db.models import F, Sum
from django.db.models import Count
from django.db.models.functions import Extract
from payment.models import *

def custom_admin_context(request):
    if request.path == '/admin/':
        interval = request.GET.get('interval', 'daily') if request.GET.get('interval') in ['daily', 'monthly', 'yearly'] else 'daily'
        user=UserProfile.objects.count()
        product=Product.objects.count()
        order=Order.objects.count()
        order_status_data = Order.objects.values('status').annotate(count=Count('status'))
        total_successful_payments = Payment.objects.filter(status='paid').aggregate(total_amount=Sum('amount'))


        total = total_successful_payments['total_amount']

        def format_currency(amount):
            return "{:,.2f}Rs".format(amount)

        # Fetch product names and total sales
        product_names = [product.name for product in Product.objects.all()]
        total_sales = [OrderItem.objects.filter(product__product_id=product).aggregate(total_sales=Sum('quantity'))['total_sales'] or 0 for product in Product.objects.all()]
        total_price = [float(OrderItem.objects.filter(product__product_id=product).aggregate(total_price=Sum(F('quantity') * F('price')))['total_price'] or 0) for product in Product.objects.all()]

        # Format the total_price as strings with currency symbol for display
        formatted_total_price = [format_currency(price) for price in total_price]

    
        labelz = [entry['status'] for entry in order_status_data]
        counts = [entry['count'] for entry in order_status_data]


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
        elif interval == 'yearly':
            sales_data = (
                Order.objects
                .annotate(year=Extract('created_at', 'year')) 
                .values('year')
                .annotate(total_revenue=Sum('total_price'))
                .order_by('year')
            )
        labels = [str(item['date'].strftime('%b %d, %Y')) if interval == 'daily'
          else str(item['month'].strftime('%b %Y')) if interval == 'monthly'
          else str(item['year']) for item in sales_data]

        revenue_data = [float(item['total_revenue']) for item in sales_data]

        chart_data = {
            'labels': labels,
            'revenue_data': revenue_data,
            'labelz':labelz,
            'counts':counts,
            'product_names': product_names,
            'total_sales': total_sales,
            'total_price': total_price, 
            'formatted_total_price': formatted_total_price, 
        }


        return {
            'chart_data': chart_data,
            'interval': interval ,
            'user_count':user,
            'product_count':product,
            'order_count':order,
            'total_payment':total,
        }
    
    return {}
