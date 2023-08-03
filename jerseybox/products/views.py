from django.shortcuts import render
from .models import Product

def product_list(request):
    products = Product.objects.all()  # Fetch all products from the database
    return render(request, 'product.html', {'products': products})

