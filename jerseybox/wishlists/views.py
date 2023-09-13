from django.http import HttpResponse
from django.shortcuts import render
from django.views import View
from products.models import * 
from django.shortcuts import redirect, render, get_object_or_404
from .models import *
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
 # Replace with your actual wishlist view name
        


class WishlistView(View):
    def get(self, request):
        if request.user.is_authenticated:
            # Try to retrieve the user's wishlist, or create one if it doesn't exist
            wishlist, created = WishlistModel.objects.get_or_create(user=request.user)
            
            # Check if wishlist is None or if it's created and product field is None
            if wishlist is not None and wishlist.product is not None:
                wishlist_items = wishlist.product.all()
            else:
                wishlist_items = []  # Initialize an empty list if wishlist or product is None

            return render(request, 'wishlist.html', {'wishlist_items': wishlist_items})
        else:
            # Handle the case when the user is not authenticated, e.g., redirect to a login page.
            return redirect('login')  # Redirect to your login page.
        
        
class AddToWishlistView(View):
    def post(self, request, product_id):
        if request.user.is_authenticated:
            # This view is only accessible to authenticated users.
            product = get_object_or_404(Product, pk=product_id)
            wishlist, created = WishlistModel.objects.get_or_create(user=request.user)
            wishlist.product.add(product)  # Assuming you have a 'products' field for the wishlist
            return redirect('wishlist_view')
        else:
            # Handle the case when the user is not authenticated, e.g., redirect to a login page.
            return redirect('login')  # Redirect to your login page.



class RemoveFromWishlistView(View):
    def post(self, request, product_id):
        if request.user.is_authenticated:
            product = get_object_or_404(Product, pk=product_id)
            wishlist = WishlistModel.objects.get(user=request.user)
            wishlist.product.remove(product)
              # Remove the product from the wishlist
            return redirect('wishlist_view')
        else:
            # Handle the case when the user is not authenticated, e.g., redirect to a login page.
            return redirect('login')