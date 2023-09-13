
from django.http import HttpResponse
from django.shortcuts import redirect, render, get_object_or_404
from django.views import View
from cart.models import *
from products.models import *


class HomeView(View):
    template="product.html"
    def get(self, request):
        
        max_to_display = 4
        featured_product_items = Product.objects.filter(is_featured=True)
        featured_items_with_images = []

        for product in featured_product_items:
            featured_image = image.objects.filter(
                product_id__product_id=product, is_featured=True
            ).first()


            if featured_image:
                featured_items_with_images.append(
                    {
                        "product": product,
                        "image_url": featured_image.image.url,
                    }
                )

        print(featured_items_with_images)

        products = Product.objects.filter(
            country_id__isnull=False, club_id__isnull=True, is_active=True
        )

        # Create a dictionary to store product images
        product_images = {}

        for product in products:
            # Get the featured image for each product
            featured_image = image.objects.filter(
                product_id__product_id=product, is_featured=True
            ).first()

            if featured_image:
                product_images[product] = featured_image.image.url
        leagues = League.objects.all()[:max_to_display]
        clubs = Club.objects.all()[:max_to_display]
        context={
                "leagues": leagues,
                "clubs": clubs,
                "featured_items_with_images": featured_items_with_images,
                "products": products,
                "product_images": product_images,
            }
        return render(
            request,
            self.template,
            context,
        )
    
    
class LeagueProductsView(View):
    template="product_list.html"
    def get(self, request, league_id):
        league = get_object_or_404(League, id=league_id)

        # Get all the clubs in the league
        clubs = Club.objects.filter(league=league)

        # Create an empty list to store product details
        all_products = []

        for club in clubs:
           
            # Retrieve products associated with the current club
            products = Product.objects.filter(club_id=club, is_active=True)

            for product in products:
                # Retrieve the related ProductItem for the current product
                product_item = ProductItem.objects.filter(product_id=product).first()

                # Retrieve related images for the current product
                images = image.objects.filter(product_id=product_item, is_featured=True)

                # Append the product, ProductItem, and images to the list
                all_products.append(
                    {
                        "product": product,
                        "product_item": product_item,
                        "images": images,
                    }
                )

        context = {
            "league": league,
            "clubs": clubs,
            "all_products": all_products,
        }

        return render(request,self.template, context)


class GenderProductsView(View):
    template_name = "gender_products.html"

    def get(self, request, gender):
        # Get the selected sorting parameter from the form
        sort_param = request.GET.get('sort', 'price_low')

        # Determine the sorting order based on the parameter
        if sort_param == 'price_high':
            sort_order = '-price'  # Sort by price (high to low)
        else:
            sort_order = 'price'   # Sort by price (low to high)

        # Fetch Product objects for the selected gender and apply sorting
        gender_products = Product.objects.filter(gender=gender, is_active=True).order_by(sort_order)

        # Fetch related images for the featured Product objects
        

        context = {
            "gender": gender,
            "gender_products": gender_products,
            
            "sort_param": sort_param,  # Pass the current sorting parameter to the template
        }

        return render(request, self.template_name, context)


class ClubProducts(View):
    template="club_products.html"
    def get(self, request, club_id):
        club = get_object_or_404(Club, id=club_id)

        # Get all the products for the club
        products = Product.objects.filter(club_id=club, is_active=True)

        # Create a dictionary to store products and their images
        products_with_images = {}

        for product in products:
            # Retrieve related images for the current product
            product_images = image.objects.filter(
                product_id__product_id=product, is_featured=True
            )

            # Add the product and its images to the dictionary
            products_with_images[product] = product_images

        context = {
            "club": club,
            "products_with_images": products_with_images,
            "product_items": ProductItem.objects.filter(
                product_id__in=products, is_active=True
            ),
        }

        return render(request,self.template, context)


class CountryProducts(View):
    template="country_products.html"
    def get(self, request, country_id):
        country = get_object_or_404(CountryModel, id=country_id)

        # Get all the products for the country
        products = Product.objects.filter(country_id=country, is_active=True)

        # Create a list to store product information including images and selling prices
        products_info = []

        for product in products:
            # Retrieve related images for the current product that are featured
            featured_images = image.objects.filter(
                product_id__product_id=product, is_featured=True
            )

            # Get the associated ProductItem for this product (if it exists)
            product_item = ProductItem.objects.filter(
                product_id=product, is_active=True
            ).first()

            # Add the product information to the list
            products_info.append(
                {
                    "product": product,
                    "images": featured_images,
                    "product_item": product_item,
                }
            )

        context = {
            "country": country,
            "products_info": products_info,
        }

        return render(request, self.template, context)




class ProductDetailView(View):
    template_name = "SingleProduct.html"

    def get(self, request, product_id):
        product = get_object_or_404(Product, id=product_id)
        images = image.objects.filter(product_id__product_id=product)[0:2]

        context = {
            "product": product,
            "images": images,
        }

        return render(request, self.template_name, context)
    
    def post(self, request, product_id):
        selected_size = request.POST.get('selected_size')
        product_item = get_object_or_404(ProductItem, product_id=product_id, size=selected_size)
        
        # Create or update the cart item with the selected product item
        if request.user.is_authenticated:
            cart, created = Cart.objects.get_or_create(user=request.user)
            cart_item, cart_item_created = CartItem.objects.get_or_create(cart=cart, product_item=product_item)
            if not cart_item_created:
                cart_item.quantity += 1
                cart_item.save()
        else:
            cart = request.session.get('cart', {})
            pk_str = str(product_item.pk)
            
            # Check if the key 'count' exists in the cart dictionary
            if pk_str in cart and 'count' in cart[pk_str]:
                cart[pk_str]['count'] += 1
            else:
                # Initialize 'count' if it doesn't exist
                cart[pk_str] = {'count': 1}
            request.session['cart'] = cart

        return redirect('cart_view')

    # def post(self, request, product_id):
    #     selected_size = request.POST.get('selected_size')
    #     product_item = get_object_or_404(ProductItem, product_id=product_id, size=selected_size)
        
    #     # Create or update the cart item with the selected product item
    #     if request.user.is_authenticated:
    #         cart, created = Cart.objects.get_or_create(user=request.user)
    #         cart_item, cart_item_created = CartItem.objects.get_or_create(cart=cart, product_item=product_item)
    #         if not cart_item_created:
    #             cart_item.quantity += 1
    #             cart_item.save()
    #     else:
    #         cart = request.session.get('cart', {})
    #         pk_str = str(product_item.pk)
            
    #         # Check if the key 'count' exists in the cart dictionary
    #         if pk_str in cart and 'count' in cart[pk_str]:
    #             cart[pk_str]['count'] += 1
    #         else:
    #             # Initialize 'count' if it doesn't exist
    #             cart[pk_str] = {'count': 1}
    #         request.session['cart'] = cart

    #     return redirect('cart_view')