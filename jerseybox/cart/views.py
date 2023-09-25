from pyexpat.errors import messages
from django.shortcuts import redirect, render,get_object_or_404
from django.views import View
from products.models import ProductItem

from cart.models import *
from django.contrib.auth.mixins import LoginRequiredMixin

from django.shortcuts import redirect, render, get_object_or_404
from django.views import View
from .models import Cart, CartItem, ProductItem

class ViewCart(View):
    def get(self, request):
        if request.user.is_authenticated:
            # Authenticated user - retrieve the cart from the database
            cart, created = Cart.objects.get_or_create(user=request.user)
            
            # Check if there are any items in the session cart
            session_cart = request.session.get('cart', {})
            if session_cart:
                # Transfer items from the session cart to the user's cart
                for product_item_id, item_data in session_cart.items():
                    product_item = get_object_or_404(ProductItem, pk=product_item_id)
                    quantity = item_data['count']
                    cart_item, cart_item_created = CartItem.objects.get_or_create(cart=cart, product_item=product_item)
                    if not cart_item_created:
                        cart_item.quantity += quantity
                        cart_item.save()
                
                # Clear the session cart after transferring items
                request.session['cart'] = {}

            cart_items = cart.cart.all().order_by('id')
        else:
            # Unauthenticated user - retrieve cart data from session
            cart_items = self._get_session_cart(request)

        # Calculate the total cost of items in the cart
        cart_total = sum(cart_item.product_item.product_id.price * cart_item.quantity for cart_item in cart_items)

        # Calculate the total cost for each specific item
        item_totals = []
        for cart_item in cart_items:
            item_total = cart_item.product_item.product_id.price * cart_item.quantity
            item_totals.append({'product_item': cart_item.product_item, 'quantity': cart_item.quantity, 'total': item_total})

        # Apply shipping charge if the total is below $1000
        shipping_charge = 0
        if cart_total < 1000:
            shipping_charge = 50  # You can adjust the shipping charge as needed

        total_cost = cart_total + shipping_charge

        return render(request, 'cart.html', {'ship':shipping_charge,'cart_items': cart_items, 'cart_total': cart_total, 'item_totals': item_totals, 'total_cost': total_cost})

    def _get_session_cart(self, request):
        cart_data = request.session.get('cart', {})
        cart_items = []

        for product_item_id, item_data in cart_data.items():
            try:
                product_item = ProductItem.objects.get(pk=product_item_id)
                quantity = item_data.get('count', 1)  # Default to 1 if 'count' is missing
                cart_item, _ = CartItem.objects.get_or_create(product_item=product_item, quantity=quantity)
                cart_items.append(cart_item)
            except ProductItem.DoesNotExist:
                # Handle the case where the ProductItem is not found gracefully
                pass

        return cart_items
    
    def post(self, request):
        if request.user.is_authenticated:
            # Authenticated user - retrieve the cart from the database
            cart, created = Cart.objects.get_or_create(user=request.user)

            # Iterate through the request.POST data to update quantities
            for key, value in request.POST.items():
                if key.startswith('quantity_'):
                    cart_item_id = key.split('_')[1]
                    try:
                        quantity = int(value)
                        if quantity >= 1:
                            cart_item = CartItem.objects.get(pk=cart_item_id, cart=cart)
                            cart_item.quantity = quantity
                            cart_item.save()
                        else:
                            # Optionally, you can remove items with quantity <= 0
                            cart_item = CartItem.objects.get(pk=cart_item_id, cart=cart)
                            cart_item.delete()
                    except (CartItem.DoesNotExist, ValueError):
                        # Handle errors here, e.g., item not found or invalid quantity
                        pass
        else:
            # Unauthenticated user - retrieve cart data from session
            cart_data = request.session.get('cart', {})

            # Iterate through the request.POST data to update quantities in the session
            for key, value in request.POST.items():
                if key.startswith('quantity_'):
                    cart_item_id = key.split('_')[1]
                    try:
                        quantity = int(value)
                        if quantity >= 1:
                            # Update the session data directly
                            cart_data[cart_item_id]['count'] = quantity
                        else:
                            # Optionally, you can remove items with quantity <= 0
                            del cart_data[cart_item_id]
                    except (KeyError, ValueError):
                        # Handle errors here, e.g., item not found or invalid quantity
                        pass
            
            # Save the updated session cart data
            request.session['cart'] = cart_data

        # Redirect to the cart view
        return redirect('cart_view')


class AddToCart(View):
    def post(self, request, pk):
        size = request.POST.get('selected_size')  # Get the selected size from the POST data
        quantity = int(request.POST.get('quantity'))  # Get the selected quantity from the POST data

        product_item = get_object_or_404(ProductItem, pk=pk, size=size)

        if product_item.stock >= quantity:
            if request.user.is_authenticated:
                # Authenticated user - add product item to the database cart with the selected size and quantity
                cart, created = Cart.objects.get_or_create(user=request.user)
                cart_item, cart_item_created = CartItem.objects.get_or_create(cart=cart, product_item=product_item)
                if not cart_item_created:
                    cart_item.quantity += quantity  # Add the quantity to the existing quantity
                else:
                    cart_item.quantity = quantity
                cart_item.save()
            else:
                # Unauthenticated user - add product item to the session cart with the selected size and quantity
                cart = request.session.get('cart', {})
                pk_str = str(pk)
                size_str = str(size)
                if pk_str in cart:
                    if size_str in cart[pk_str]:
                        cart[pk_str][size_str]['count'] += quantity  # Add the quantity to the existing quantity
                request.session['cart'] = cart

            return redirect('product_detail', pk=pk)
        else:
            # Not enough stock - handle this case (e.g., display an error message)
            error_message = "Not enough stock available for the selected size and quantity."
            return render(request, 'product_detail.html', {'product_item': product_item, 'error_message': error_message})

        


class RemoveFromCart(View):
    def get(self, request, product_item_id):
        if request.user.is_authenticated:
            # Authenticated user - remove the item from the database cart
            product_item = get_object_or_404(ProductItem, id=product_item_id)
            cart, created = Cart.objects.get_or_create(user=request.user)
            cart_item = cart.cartitem.filter(product_item=product_item).first()
            if cart_item:
                if cart_item.quantity > 1:
                    cart_item.quantity -= 1
                    cart_item.save()
                else:
                    cart_item.delete()
        else:
            # Unauthenticated user - remove the item from the session cart
            cart = request.session.get('cart', {})
            pk_str = str(product_item_id)
            if pk_str in cart:
                if cart[pk_str]['count'] > 1:
                    cart[pk_str]['count'] -= 1
                else:
                    del cart[pk_str]
            request.session['cart'] = cart

        return redirect('cart_view')









# class AddToCart(View):
#     def get(self, request, pk):
#         if request.user.is_authenticated:
#             # Authenticated user - add product item to the database cart
#             product_item = get_object_or_404(ProductItem, pk=pk)
#             cart, created = Cart.objects.get_or_create(user=request.user)
#             cart_item, cart_item_created = CartItem.objects.get_or_create(cart=cart, product_item=product_item)
#             if not cart_item_created:
#                 cart_item.quantity += 1
#                 cart_item.save()
#         else:
#             # Unauthenticated user - add product item to the session cart
#             cart = request.session.get('cart', {})
#             # Convert pk to a string when using it as a dictionary key
#             pk_str = str(pk)
#             if pk_str in cart:
#                 cart[pk_str]['count'] += 1
#             else:
#                 cart[pk_str] = {'count': 1}
#             request.session['cart'] = cart

#         return redirect('cart_view')
