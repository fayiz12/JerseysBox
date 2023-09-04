
import hashlib
from django.http import Http404
from django.shortcuts import redirect, render, get_object_or_404
from django.urls import reverse

from .models import UserProfile
from django.contrib import messages
from django.contrib.auth import authenticate, login as auth_login,logout
from .email import *
from django.core.cache import cache
from products.models import *
from django.views import View
import random
from django.utils.http import urlsafe_base64_encode,urlsafe_base64_decode



class HomeView(View):
    def get(self, request):
      max_to_display = 4
      featured_product_items = ProductItem.objects.filter(product_id__is_featured=True)
      featured_items_with_images = []

      for product_item in featured_product_items:
        featured_images = product_item.image.filter(is_featured=True)
        for featured_image in featured_images:
            featured_items_with_images.append({
                'product_item': product_item,
                'image_url': featured_image.image.url
            })
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
      clubs=Club.objects.all()[:max_to_display]
      return render(request, 'product.html', {'leagues': leagues,'clubs':clubs,'featured_items_with_images': featured_items_with_images,'products':products,'product_images': product_images})




class SignupView(View):
    def get(self, request):
        return render(request, "signup.html")

    def post(self, request):
        email = request.POST.get("email")
        name = request.POST.get("username")
        # mobile = request.POST.get("mobile")
        pass1 = request.POST.get("pass1")
        pass2 = request.POST.get("pass2")

        userobj = UserProfile.objects.filter(email=email)
        if userobj.exists():
            messages.warning(
                request, "You are already registered. Please login.")
            return redirect("register")

        if pass1 != pass2:
            messages.warning(request, "Password does not match.")
            return redirect("register")

        otp = str(random.randint(100000, 999999))
        send_otp_email(email, name, otp)
        key = hashlib.sha256(email.encode()).hexdigest()
        cache.set(key, {'email': email, 'name': name,
                  'password': pass1, 'otp': otp}, timeout=600)
        return redirect("otp", key=key)


class VerifyOtpView(View):
    def get(self, request, key):
        # Render the OTP verification form
        return render(request, "otp.html", {'key': key})

    def post(self, request, key):
        receivedotp = request.POST.get("otp")

        signup_data = cache.get(key)
        print(signup_data)
        if not signup_data:
            messages.warning(request, 'OTP expired or invalid')
            return redirect('otp', key=key)
        otp = signup_data.get('otp')
        name = signup_data.get('name')
        email = signup_data.get('email')
        password = signup_data.get('password')
        print(receivedotp, otp)
        if receivedotp != otp:
            messages.warning(request, "OTP mismatch")
            return redirect("otp", key=key)

        user = UserProfile.objects.create_user(
            username=name, email=email, password=password
        )
        user.save()
        cache.delete(key)
        return redirect("login")

class ResendOTP(View):
  def get(self, request, key):
    signup_data = cache.get(key)
    if signup_data:
      email = signup_data.get('email')
      name = signup_data.get('name')
      otp = str(random.randint(100000, 999999))
      print(otp)
      send_otp_email(email, name, otp)
      signup_data['otp'] = otp
      existing_timeout = signup_data.get('timeout', None)
      cache.set(key, signup_data, timeout=existing_timeout)
      return redirect('otp', key=key)
    return redirect('signup')

class ForgotPassword(View):

  def get(self, request):
    return render(request, 'password_forgot_form.html')
  
  def post(self, request):
    email=request.POST.get('email')
    try:
      user = UserProfile.objects.get(email=email)
    except:
      messages.warning(request , 'You are not registerd, Please sign up')
      return redirect('register')
    encrypt_id = urlsafe_base64_encode(str(user.pk).encode())
    reset_link = f"{request.scheme}://{request.get_host()}{reverse('reset', args=[encrypt_id])}"
    cache_key = f"reset_link_{encrypt_id}"
    cache.set(cache_key, {'reset_link':reset_link}, timeout=60) 
    reset_password_email(email, reset_link)
    messages.success(request, 'Password reset link sent to your email.')
    return redirect('login')

class UserResetPassword(View):
  
  def get(self, request, encrypt_id):
    cache_key = f"reset_link_{encrypt_id}"
    cache_data = cache.get(cache_key)
    if not cache_data:
      raise Http404("Reset link has expired")
    reset_id = cache_data.get('reset_link')
    return render(request, 'password_reset.html',{'reset':reset_id})

  def post(self, request, encrypt_id):
    cache_key = f"reset_link_{encrypt_id}"
    id = str(urlsafe_base64_decode(encrypt_id), 'utf-8')
    user = UserProfile.objects.get(pk=id)
    new_password = request.POST.get('pass1')
    user.set_password(new_password)
    user.save()
    cache.delete(cache_key)
    messages.success(request, 'Password reset successful. You can now log in with your new password.')
    return redirect('login')

class LoginView(View):
    def post(self, request):
        name = request.POST.get("username")
        pass1 = request.POST.get("pass1")

        user = authenticate(request, username=name, password=pass1)
        if user is not None:
            auth_login(request, user)
            return redirect("home")
        else:
            return redirect("login")

    def get(self, request):
        return render(request, "login.html")




class UserSignout(View):

  def get(self, request):
    logout(request)
    return redirect('login')





class LeagueProductsView(View):
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
                all_products.append({
                    'product': product,
                    'product_item': product_item,
                    'images': images,
                })
        
        context = {
            'league': league,
            'clubs': clubs,
            'all_products': all_products,
        }
        
        return render(request, 'product_list.html', context)


class GenderProductsView(View):
    template_name = 'gender_products.html'

    def get(self, request, gender):
        # Fetch featured ProductItem objects for the selected gender
        gender_products = ProductItem.objects.filter(gender=gender, is_active=True)

        # Fetch related images for the featured ProductItem objects
        featured_images = image.objects.filter(product_id__in=gender_products, is_featured=True)

        context = {
            'gender': gender,
            'gender_products': gender_products,
            'featured_images': featured_images,
        }

        return render(request, self.template_name, context)


class club_products(View):   
  def get(self,request, club_id):
      club = get_object_or_404(Club, id=club_id)
      
      # Get all the products for the club
      products = Product.objects.filter(club_id=club, is_active=True)
      
      # Create a dictionary to store products and their images
      products_with_images = {}
      
      for product in products:
          # Retrieve related images for the current product
          product_images = image.objects.filter(product_id__product_id=product, is_featured=True)
          
          # Add the product and its images to the dictionary
          products_with_images[product] = product_images
      
      context = {
          'club': club,
          'products_with_images': products_with_images,
          'product_items': ProductItem.objects.filter(product_id__in=products, is_active=True),
      }
      
      return render(request, 'club_products.html', context)

class country_products(View):
  def get(self,request, country_id):
      country = get_object_or_404(CountryModel, id=country_id)
      
      # Get all the products for the country
      products = Product.objects.filter(country_id=country, is_active=True)
      
      # Create a list to store product information including images and selling prices
      products_info = []
      
      for product in products:
          # Retrieve related images for the current product that are featured
          featured_images = image.objects.filter(product_id__product_id=product, is_featured=True)
          
          # Get the associated ProductItem for this product (if it exists)
          product_item = ProductItem.objects.filter(product_id=product, is_active=True).first()
          
          # Add the product information to the list
          products_info.append({
              'product': product,
              'images': featured_images,
              'product_item': product_item,
          })
      
      context = {
          'country': country,
          'products_info': products_info,
      }
      
      return render(request, 'country_products.html', context)




class ProductDetailView(View):
    template_name = 'SingleProduct.html'

    def get(self, request, product_id):
        product_item = ProductItem.objects.get(product_id=product_id)
        images = image.objects.filter(product_id=product_item)
        # You can fetch additional information related to the product here if needed

        context = {
            'product': product_item,
            'images':images,
        }

        return render(request, self.template_name, context)