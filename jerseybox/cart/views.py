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

            cart_items = cart.cartitem_set.all().order_by('id')
        else:
            # Unauthenticated user - retrieve cart data from session
            cart_items = self._get_session_cart(request)

        return render(request, 'cart.html', {'cart_items': cart_items})

    def _get_session_cart(self, request):
        cart_data = request.session.get('cart', {})
        cart_items = []

        for product_item_id, item_data in cart_data.items():
            product_item = get_object_or_404(ProductItem, pk=product_item_id)
            quantity = item_data['count']
            cart_items.append({'product_item': product_item, 'quantity': quantity})

        return cart_items


class AddToCart(View):
    def get(self, request, pk):
        size = request.GET.get('size')  # Get the selected size from the query parameter
        if request.user.is_authenticated:
            # Authenticated user - add product item to the database cart with the selected size
            product_item = get_object_or_404(ProductItem, pk=pk, size=size)
            cart, created = Cart.objects.get_or_create(user=request.user)
            cart_item, cart_item_created = CartItem.objects.get_or_create(cart=cart, product_item=product_item)
            if not cart_item_created:
                cart_item.quantity += 1
                cart_item.save()
        else:
            # Unauthenticated user - add product item to the session cart with the selected size
            cart = request.session.get('cart', {})
            # Convert pk and size to strings when using them as dictionary keys
            pk_str = str(pk)
            size_str = str(size)
            if pk_str in cart:
                if size_str in cart[pk_str]:
                    cart[pk_str][size_str]['count'] += 1
                else:
                    cart[pk_str][size_str] = {'count': 1}
            else:
                cart[pk_str] = {size_str: {'count': 1}}
            request.session['cart'] = cart

        return redirect('cart_view')

class RemoveFromCart(View):
    def get(self, request, product_item_id):
        if request.user.is_authenticated:
            # Authenticated user - remove the item from the database cart
            product_item = get_object_or_404(ProductItem, id=product_item_id)
            cart, created = Cart.objects.get_or_create(user=request.user)
            cart_item = cart.cartitem_set.filter(product_item=product_item).first()
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
