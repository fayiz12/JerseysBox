
from venv import logger
from django.http import HttpResponse
from django.shortcuts import redirect, render, get_object_or_404
from django.views import View
from cart.models import *
from products.models import *
from categories.models import *
from order.models import *
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.urls import reverse_lazy
from django.views.generic.edit import FormView
from order.forms import AddressForm
from django.views.generic.edit import UpdateView
import razorpay
from django.conf import settings
from coupon.models import  *
from django.contrib import messages
from django.utils import timezone
from datetime import date
from django.template.loader import render_to_string
from xhtml2pdf import pisa
from payment.models import *
from decimal import Decimal
from products.breadcrumbs import *






class HomeView(View):
    template="product.html"
    def get(self, request):
        url = request.path

        # Generate the breadcrumbs for the current URL
        breadcrumbs = get_breadcrumbs(url)
        max_to_display = 4
        featured_product_items = Product.objects.filter(is_featured=True)[:4]
        featured_items_with_images = []

        for product in featured_product_items:
            featured_image = Image.objects.filter(
                product=product
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
                product=product, is_featured=True
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
                "breadcrumbs": breadcrumbs
            }
        return render(
            request,
            self.template,
            context,
        )
    


    
class LeagueProductsView(View):
    
    template_name = "product_list.html"  # Corrected the template attribute name
    items_per_page = 10  # Adjust the number of items per page as needed

    def get(self, request, league_id):
        breadcrumbs = [{"title": "league_products", "url": "/"}]
        sort_param = request.GET.get('sort', 'price_low')
        selected_product_type = request.GET.get('product_type')
        selected_gender = request.GET.get('gender')
        selected_year = request.GET.get('years')
        
        if sort_param == 'name':
            sort_order = 'name' 
        elif sort_param == 'name_desc':
            sort_order = '-name' 
        elif sort_param == 'price_high':
            sort_order = '-price'  
        else:
            sort_order = 'price'

        league = get_object_or_404(League, id=league_id)
        clubs = Club.objects.filter(league=league)
        club_ids = clubs.values_list('id', flat=True)  # Get club IDs
        
        # Fix variable name: club_products instead of league_products
        club_products = Product.objects.filter(club_id__in=club_ids).order_by(sort_order)
        
        if selected_product_type:
            club_products = club_products.filter(type=selected_product_type)

        # Fix variable name: club_products instead of gender_products
        if selected_gender:
            club_products = club_products.filter(gender=selected_gender)

        if selected_year:
            club_products = club_products.filter(year=selected_year)

        # Fetch unique years for the filter
        years = club_products.values_list('year', flat=True).distinct()

        # Implement pagination
        page_number = request.GET.get('page')
        paginator = Paginator(club_products, self.items_per_page)
        page = paginator.get_page(page_number)


        context = {
            "years": years,
            "page":page,
            "league": league,
            "clubs": clubs,
            "breadcrumbs": breadcrumbs,

        }

        return render(request,self.template_name, context)
    



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

        # Filter data based on the selected filters
        
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
    items_per_page = 4
    def get(self, request, club_id):
        sort_param = request.GET.get('sort', 'price_low')
        selected_gender = request.GET.get('gender')
        # Get the selected product type (Home/Away)
        selected_product_type = request.GET.get('product_type') 
        selected_year=request.GET.get('years')
        if sort_param == 'name':
            sort_order = 'name'  # Sort by name (ascending)
        elif sort_param == 'name_desc':
            sort_order = '-name'  # Sort by name (descending)
        elif sort_param == 'price_high':
            sort_order = '-price'  # Sort by price (high to low)
        else:
            sort_order = 'price' 
            

        club = get_object_or_404(Club, id=club_id)
        products = Product.objects.filter(club_id=club, is_active=True).order_by(sort_order)

        if selected_gender:
            products = products.filter(gender=selected_gender)

    
        if selected_product_type:
            products = products.filter(type=selected_product_type)
            

        if selected_year:
            products = products.filter(year=selected_year)

        years = Product.objects.values_list('year', flat=True).distinct()

        # Implement pagination
        page_number = request.GET.get('page')
        paginator = Paginator(products, self.items_per_page)
        page = paginator.get_page(page_number)
        context = {
            "club": club,
            'years':years,
            "page": page,
            "products_with_images": products,
            "product_items": ProductItem.objects.filter(
                product_id__in=products, is_active=True
            ),
        }

        return render(request,self.template, context)


class CountryProducts(View):
    template="country_products.html"
    items_per_page=10
    def get(self, request, country_id):
        sort_param = request.GET.get('sort', 'price_low')
        selected_gender = request.GET.get('gender')
        # Get the selected product type (Home/Away)
        selected_product_type = request.GET.get('product_type') 
        selected_year=request.GET.get('years')
        if sort_param == 'name':
            sort_order = 'name'  # Sort by name (ascending)
        elif sort_param == 'name_desc':
            sort_order = '-name'  # Sort by name (descending)
        elif sort_param == 'price_high':
            sort_order = '-price'  # Sort by price (high to low)
        else:
            sort_order = 'price' 
        country = get_object_or_404(CountryModel, id=country_id)
        products = Product.objects.filter(country_id=country, is_active=True).order_by(sort_order)
        

        if selected_gender:
            products = products.filter(gender=selected_gender)

    
        if selected_product_type:
            products = products.filter(type=selected_product_type)
            

        if selected_year:
            products = products.filter(year=selected_year)

        years = Product.objects.values_list('year', flat=True).distinct()

        # Implement pagination
        page_number = request.GET.get('page')
        paginator = Paginator(products, self.items_per_page)
        page = paginator.get_page(page_number)

        context = {
            "page":page,
            "years":years,
            "country": country,
            "products": products,
        }

        return render(request, self.template, context)




class ProductDetailView(View):
    template_name = "SingleProduct.html"

    def get(self, request, product_id):
        breadcrumbs = [{"title": "league_products", "url": "/"}]
        product = get_object_or_404(Product, id=product_id)
        images = Image.objects.filter(product_id=product)[0:2]
        

        context = {
            "product": product,
            "images": images,
            "breadcrumbs": breadcrumbs,
        }

        return render(request, self.template_name, context)
    
    def post(self, request, product_id):
        selected_size = request.POST.get('selected_size')
        product_item = get_object_or_404(ProductItem, product_id=product_id, size=selected_size)
        quantity = int(request.POST.get('quantity', 1))  # Get the selected quantity or default to 1

        # Create or update the cart item with the selected product item
        if request.user.is_authenticated:
            cart, created = Cart.objects.get_or_create(user=request.user)
            cart_item, cart_item_created = CartItem.objects.get_or_create(cart=cart, product_item=product_item)
            
            # If the cart item already exists, add the specified quantity to the existing quantity
            if not cart_item_created:
                if quantity<5:
                    cart_item.quantity += quantity
                 # Add this line to check the message tag
                    messages.success(request, "Added to cart")
                else:
                    messages.error(request,'choose quantity less than 5')

            else:
                if quantity<5:

                    cart_item.quantity = quantity  # Set the quantity to the desired value
                 # Add this line to check the message tag
                    messages.success(request, "Added to cart")
                else:
                    messages.error(request,'choose quantity less than 5')

            cart_item.save()
        else:
            cart = request.session.get('cart', {})
            pk_str = str(product_item.id)
            
            # Check if the key 'count' exists in the cart dictionary
            if pk_str in cart and 'count' in cart[pk_str]:
                if quantity<5:
                    cart[pk_str]['count'] += quantity
                else:
                    messages.error(request,'choose quantity less than 5') # Add the specified quantity to the existing quantity
            else:
                # Initialize 'count' if it doesn't exist
                if quantity<5:
                    cart[pk_str] = {'count': quantity}
                else:
                    messages.error(request,'choose quantity less than 5')
            
            request.session['cart'] = cart

        return redirect(request.META.get('HTTP_REFERER'))








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


class CheckoutView(View):
    def get(self, request):
        if not request.user.is_authenticated:
            return redirect('login')
        user = request.user
        try:
            current_user=UserProfile.objects.get(pk=user.pk)
            cart = Cart.objects.get(user=user)
            cart_items = CartItem.objects.filter(cart=cart)
            coupons=Coupon.objects.all()
            addresses = Address.objects.filter(user=user).order_by('-created_at')[:4]
            client = razorpay.Client(auth=(settings.RAZORPAY_API_KEY,settings.RAZORPAY_API_SECRET))
            payment_order = client.order.create(dict(amount = request.user.cart.final_price*100, currency = "INR", payment_capture = 1))
            payment_order_id = payment_order['id']
           
        except:
         
            return redirect(request.META.get('HTTP_REFERER'))
        context={"cart": cart,
                "current_user":current_user,
                "cart_items": cart_items,
                'addresses':addresses, 
                'cart':cart, 
                'cart_items':cart_items,
                'payment_api_key':settings.RAZORPAY_API_KEY,
                'order_id':payment_order_id}
        
        return render(request, "checkout.html", context)
    
    
    def post(self, request):
        client = razorpay.Client(auth=(settings.RAZORPAY_API_KEY, settings.RAZORPAY_API_SECRET))

        print('dfghj,')
        user = request.user
        selected_address_id = request.POST.get('selectedAddress')
        selected_payment_method = request.POST.get('payment_method')
        payment_order_id=request.POST.get('order_id')
        print(selected_payment_method,'strsrs')
        print(payment_order_id,'sd')

        cart = get_object_or_404(Cart, user=user)
        cart_items = CartItem.objects.filter(cart=cart)
        selected_address = Address.objects.get(id=selected_address_id)

        
        if selected_address and selected_payment_method and cart and cart_items:

            order = Order.objects.create(
                user=user,
                total_price=cart.final_price,
                sub_total=cart.total,
                coupon_discount=cart.coupon_discount,
                shipping_address=selected_address,
                payment_mode=selected_payment_method,
            )

            for cart_item in cart_items:
                OrderItem.objects.create(
                    order=order,
                    product=cart_item.product_item,
                    quantity=cart_item.quantity,
                    price=cart_item.product_item.product_id.price,  
                    status='processing',
                )
            if selected_payment_method == 'razorpay':
                payment_order=client.order.fetch(payment_order_id)
                print(payment_order)
                Payment.objects.create(
                    user=user,
                    transaction_id=payment_order['id'],
                    amount=Decimal(str(payment_order['amount'])) / 100 ,
                    status=payment_order['status'],
                )
            elif selected_payment_method == 'cash_on_delivery':

                Payment.objects.create(
                    user=user,
                    transaction_id='COD', 
                    amount=order.total_price,
                    status='pending',
                )

            cart.coupon_discount = 0
            cart.save()
            cart_items.delete()
            
            

            data = {
            "orders": order,
            "user": user,
            "address": selected_address,

            
            }
            return render(request, 'order_confirmed.html', {'data': data})

            



class UserInvoice(View):
    def get(self, request, pk):
        if not request.user.is_authenticated:
            return redirect('login')

        template_name = 'invoice_template.html'
        order = request.user.order.get(id=pk)
        context = {'order': order}
        html_content = render_to_string(template_name, context)
        response = HttpResponse(content_type='application/pdf')
        response['Content-Disposition'] = 'attachment; filename="invoice.pdf.pdf"'
        pisa_status = pisa.CreatePDF(html_content, dest=response, encoding='utf-8')
        if pisa_status:
            return response
        return None

    
    

class AddAddressView(FormView):
    template_name = 'add_address.html'
    form_class = AddressForm  
    success_url = reverse_lazy('checkout')

    def form_valid(self, form):
        user = self.request.user
        address = form.save(commit=False)
        address.user = user
        address.save()
        return super().form_valid(form)
    


# class UpdateAddressView(UpdateView):
#     model = Address
#     form_class = AddressForm  # Use the custom form
#     template_name = 'update_address.html'
#     success_url = reverse_lazy('checkout')

#     def get_object(self, queryset=None):
#         address_id = self.kwargs['address_id']
#         return get_object_or_404(Address, id=address_id, user=self.request.user)
    

class ApplyCouponView(View):
    def post(self, request):
        if not request.user.is_authenticated:
            return redirect('login')
        coupon_code = request.POST.get('coupon_code')
        cart = request.user.cart
        cart.coupon_discount=0

        try:
            # Check if a coupon with the provided code exists
            coupon = Coupon.objects.get(code=coupon_code)
        except Coupon.DoesNotExist:
            messages.error(request, 'Invalid coupon code.')  # Invalid coupon message
            return redirect(request.META.get('HTTP_REFERER'))

        # Check if the coupon has expired
        if coupon.expiry_date and coupon.expiry_date < timezone.now().date():
            messages.error(request, 'Coupon has expired.')  # Coupon expired message
        else:
            # Check if the cart total meets the coupon requirements
            if cart.total > coupon.discount_value:
                cart.coupon_discount = coupon.discount_value
                cart.final_price = cart.total - coupon.discount_value
                messages.success(request,'coupon Applied ')
            else:
                messages.warning(request, 'Coupon applied, but it does not meet the cart total requirement.')

        cart.save()
        return redirect(request.META.get('HTTP_REFERER'))
    

class OrderHistoryView(View):
    
    def get(self,request):
        if not request.user.is_authenticated:
            return redirect('login')
        template='order_history.html'
        orders=Order.objects.filter(user=request.user)
            
        context={
            'orders':orders,
        }
        return render(request,template,context)
    # def post(self, request):
    #     # Check if a coupon with the provided code exists
    #     try:
    #         coupon = request.POST.get('coupon_code')
    #         print(coupon,'rdydejyey6')
    #     except Coupon.DoesNotExist:
    #         pass 
        
    #     cart = request.user.cart
    #     if coupon := Coupon.objects.filter(code=coupon).first():
    #         if cart.total > coupon.discount_value:
    #             cart.coupon_discount = coupon.discount_value
    #             cart.final_price = cart.total - coupon.discount_value
    #             cart.save()
    #         else: 
    #             cart.coupon_discount = 0
    #             cart.final_price = cart.total
    #             cart.save() 
    #     else:
    #         cart.coupon_discount = 0
    #         cart.final_price = cart.total
    #         cart.save()
    #     return redirect(request.META.get('HTTP_REFERER'))


class TrackView(View):
    
    def get(self,request,pk):
        template='track.html'
        orders=Order.objects.get(id=pk)
            
        context={
            'orders':orders,
        }
        return render(request,template,context)



