from django.shortcuts import render, redirect
from django.views import View
from .models import Cart, CartItem, Address, Order, OrderItem
from users.models import UserProfile
from products.models import ProductItem
import uuid

class PlaceOrderView(View):
    def post(self, request):
        user = request.user

        # Get the user's cart
        try:
            cart = Cart.objects.get(user=user)
        except Cart.DoesNotExist:
            # Handle the case where the cart doesn't exist
            return redirect('checkout')  # Redirect to the checkout page with a message

        # Get the selected address from the request (you may want to implement this in your HTML form)
        address_id = request.POST.get('selectedAddress')

        try:
            selected_address = Address.objects.get(id=address_id, user=user)
        except Address.DoesNotExist:
            # Handle the case where the selected address doesn't exist
            return redirect('checkout')  # Redirect to the checkout page with a message

        # Calculate the total price based on cart items
        total_price = sum(item.product_item.product_id.price * item.quantity for item in cart.cartitem.all())

        # Get the selected payment method from the request (e.g., 'cash_on_delivery' or 'razorpay')
        payment_method = request.POST.get('payment_method')

        # Create an order
        order = Order.objects.create(
            user=user,
            total_price=total_price,
            payment_method=payment_method,
            shipping_address=selected_address
        )

        # Move cart items to order items
        for cart_item in cart.cartitem.all():
            OrderItem.objects.create(
                order=order,
                product=cart_item.product_item,
                quantity=cart_item.quantity,
                price=cart_item.product_item.product_id.price,
            )

        # Clear the user's cart
        cart.cartitem.all().delete()

        # Redirect to a payment page if the payment method is 'razorpay'
        # if payment_method == 'razorpay':
        #     # You'll need to implement the Razorpay payment flow here
        #     # Generate a Razorpay order and obtain the order ID
        #     razorpay_order_id = generate_razorpay_order(order)
        #     return render(request, 'razorpay_payment.html', {'order': order, 'razorpay_order_id': razorpay_order_id})
        
        # Redirect to a confirmation page for cash on delivery
        return render(request, 'order_confirmation.html', {'order': order})
