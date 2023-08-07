from django.shortcuts import redirect, render,get_object_or_404
from django.contrib.auth.forms import UserCreationForm
from .models import UserProfile,UserProfileManager
from django.contrib import messages
from django.contrib.auth import authenticate,login as auth_login
from .email import send_otp_email
from django.core.cache import cache
from products.models import *
from django.views import View





class HomeView(View):
    def get(self,request):
        products = Product.objects.all()
        return render(request, 'product.html', {'products': products})


class ProductDetailView(View):
    def get(self, request, id):
        details = get_object_or_404(Product, id=id)
        return render(request, 'SingleProduct.html', {'product': details})

class SignupView(View):
    def post(self, request):
        email = request.POST.get('email')
        name = request.POST.get('username')
        mobile = request.POST.get('mobile')
        pass1 = request.POST.get('pass1')
        pass2 = request.POST.get('pass2')
        
        userobj = UserProfile.objects.filter(email=email)
        if userobj.exists():
            messages.warning(request, 'You are already registered. Please login.')
            return redirect('register')

        if pass1 != pass2:
            messages.warning(request, 'Password does not match.')
            return redirect('register')

        send_otp_email(email, name, mobile, pass1)
        return redirect('otp')

    def get(self, request):
        return render(request, 'signup.html')



class VerifyOtpView(View):
    def post(self, request):
        receivedotp = request.POST.get('otp')
        email = request.POST.get('email')  
        
        cache_key = f'cache_data_{email}'  
        
        try:
            signup_data = cache.get(cache_key)
            cached_otp = signup_data['otp']
            name = signup_data['name']
            mobile = signup_data['mobile']
            password = signup_data['password']
        except:
            messages.warning(request, 'OTP has Expired')
            return redirect('verify_otp')
        
        if receivedotp != cached_otp:
            messages.warning(request, 'OTP mismatch')
            return redirect('verify_otp')

        UserProfile.objects.create_user(username=name, email=email, mobile=mobile, password=password)
        return redirect('login')




class LoginView(View):
    def post(self, request):
        name = request.POST.get('username')
        pass1 = request.POST.get('pass1')

        user = authenticate(request, username=name, password=pass1)
        if user is not None:
            auth_login(request, user)
            return redirect('home')
        else:
            return redirect('login')

    def get(self, request):
        return render(request, 'login.html')


