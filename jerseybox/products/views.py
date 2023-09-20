
from django.http import HttpResponse
from django.shortcuts import redirect, render, get_object_or_404
from django.views import View
from cart.models import *
from products.models import *
from categories.models import *
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

class HomeView(View):
    template="product.html"
    def get(self, request):
        
        max_to_display = 4
        featured_product_items = Product.objects.filter(is_featured=True)
        featured_items_with_images = []

        for product in featured_product_items:
            featured_image = Image.objects.filter(
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
            featured_image = Image.objects.filter(
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
                images = Image.objects.filter(product_id=product_item, is_featured=True)

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
    items_per_page = 4  # Define how many items you want to display per page
    
    def get(self, request, gender):
        # Get the selected sorting parameter from the form
        sort_param = request.GET.get('sort', 'price_low')

        # Get the selected product type (Home/Away)
        selected_product_type = request.GET.get('product_type')

        # Get the selected category (Country/Club)
        selected_category = request.GET.get('category')
        
        selected_year=request.GET.get('years')
        if sort_param == 'name':
            sort_order = 'name'  # Sort by name (ascending)
        elif sort_param == 'name_desc':
            sort_order = '-name'  # Sort by name (descending)
        elif sort_param == 'price_high':
            sort_order = '-price'  # Sort by price (high to low)
        else:
            sort_order = 'price'   # Sort by price ( high)

        # Fetch Product objects for the selected gender and apply filters/sorting
        gender_products = Product.objects.filter(gender=gender, is_active=True).order_by(sort_order)

        # Apply product type filter
        if selected_product_type:
            gender_products = gender_products.filter(type=selected_product_type)

        # Apply category filter
        if selected_category:
            gender_products = gender_products.filter(category=selected_category)

        if selected_year:
            gender_products = gender_products.filter(year=selected_year)

        # Fetch unique years for the filter
        years = Product.objects.values_list('year', flat=True).distinct()

        # Implement pagination
        page_number = request.GET.get('page')
        paginator = Paginator(gender_products, self.items_per_page)
        page = paginator.get_page(page_number)

        context = {
            "gender": gender,
            "page": page,  # Use the paginated queryset
            "years": years,
            "sort_param": sort_param,
            "selected_product_type": selected_product_type,
            "selected_category": selected_category,
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
            product_images = Image.objects.filter(
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
            featured_images = Image.objects.filter(
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
        images = Image.objects.filter(product_id__product_id=product)[0:2]

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