from django.conf import settings
from django.shortcuts import render, redirect
from django.views import View
import razorpay
from order.models import *


class PaymentView(View):
    def get(self, request, order_id):
        # Retrieve order details and calculate the amount
        order = Order.objects.get(id=order_id)
        amount = int(order.total_price * 100)  # Razorpay expects the amount in paisa

        client = razorpay.Client(auth=(settings.RAZORPAY_API_KEY, settings.RAZORPAY_API_SECRET))
        payment = client.order.create({'amount': amount, 'currency': 'INR'})

        return render(request, 'payment.html', {'payment': payment})

    def post(self, request, order_id):
        # Handle the Razorpay callback and verify the payment
        razorpay_payment_id = request.POST.get('razorpay_payment_id')
        razorpay_signature = request.POST.get('razorpay_signature')

        client = razorpay.Client(auth=(settings.RAZORPAY_API_KEY, settings.RAZORPAY_API_SECRET))
        params_dict = {
            'razorpay_payment_id': razorpay_payment_id,
            'razorpay_order_id': request.POST.get('razorpay_order_id'),
            'razorpay_signature': razorpay_signature,
        }

        try:
            client.utility.verify_payment_signature(params_dict)
            # Payment is verified, update your order status as paid
            order = Order.objects.get(id=order_id)
            order.status = 'Paid'
            order.save()
            return redirect('order_confirmation')
        except razorpay.errors.SignatureVerificationError:
            # Payment verification failed
            return redirect('payment_failed')


