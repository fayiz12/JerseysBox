from django.contrib import messages
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
       
        shipping_charge = 0  # You can adjust the shipping charge as needed

        total_cost = cart_total + shipping_charge

        return render(request, 'cart.html', {'ship':shipping_charge,'cart_items': cart_items, 'cart_total': cart_total, 'item_totals': item_totals, 'total_cost': total_cost})

    def _get_session_cart(self, request):
        cart_data = request.session.get('cart', {})
        cart_items = []

        for product_item_id, item_data in cart_data.items():
            try:
                product_item = ProductItem.objects.get(pk=product_item_id)
                quantity = item_data.get('count', 1)  # Default to 1 if 'count' is missing
                
                # Create a temporary cart object for unauthenticated users
                temp_cart, _ = Cart.objects.get_or_create(session_id=request.session.session_key)
                
                cart_item, _ = CartItem.objects.get_or_create(cart=temp_cart, product_item=product_item, quantity=quantity)
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
                            if quantity<5:
                                cart_item = CartItem.objects.get(pk=cart_item_id, cart=cart)
                                cart_item.quantity = quantity
                                cart_item.save()
                                
                            else:
                                messages.error(request, "invalid quantity")
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

            print("Before Update - cart_data:", cart_data)
            
            # Iterate through the request.POST data to update quantities in the session
            for key, value in request.POST.items():
                if key.startswith('quantity_'):
                    cart_item_id = key[len('quantity_'):]
                    cart_item = CartItem.objects.get(id=cart_item_id)
                    pk_str = str(cart_item.product_item.id)
                   
                  
                    print("dsf",cart_item)

                    try:
                        quantity = int(value)

                        # Check if cart_item_id exists in cart_data
                        if pk_str in cart_data:
                            if quantity >= 1 and quantity < 5:
                                # Update the session data directly
                                cart_data[pk_str]['count'] = quantity
                                print(f"Updated quantity for {pk_str} to {quantity}")
                            else:
                                messages.error(request, "Invalid quantity")
                        else:
                            print(f"Item with ID {cart_item_id} not found in cart_data.")
                    except (KeyError, ValueError):
                        # Handle errors here, e.g., item not found or invalid quantity
                        pass

            # Save the updated session cart data
            request.session['cart'] = cart_data
            print("After Update - cart_data:", cart_data)

        # Redirect to the cart view
        return redirect('cart_view')




class RemoveFromCart(View):
    def get(self, request, product_item_id):
        if request.user.is_authenticated:
            # Authenticated user - remove the item from the database cart
            product_item = get_object_or_404(ProductItem, id=product_item_id)
            cart, created = Cart.objects.get_or_create(user=request.user)
            cart_item = CartItem.objects.filter(product_item=product_item).first()
            if cart_item:
                messages.success(request, "removed from cart")
                cart_item.delete()
        else:
            # Unauthenticated user - remove the item from the session cart
            cart = request.session.get('cart', {})
            pk_str = str(product_item_id)
            if pk_str in cart:
                if cart[pk_str]['count'] > 1:
                    del cart[pk_str]
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
