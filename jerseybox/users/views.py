import hashlib
from django.shortcuts import redirect, render, get_object_or_404

from .models import UserProfile
from django.contrib import messages
from django.contrib.auth import authenticate, login as auth_login
from .email import send_otp_email
from django.core.cache import cache
from products.models import *
from django.views import View
import random


class HomeView(View):
    def get(self, request):
        products = Product.objects.all()
        return render(request, "product.html", {"products": products})


class ProductDetailView(View):
    def get(self, request, id):
        details = get_object_or_404(Product, id=id)
        return render(request, "SingleProduct.html", {"product": details})


class SignupView(View):
    def get(self, request):
        return render(request, "signup.html")

    def post(self, request):
        email = request.POST.get("email")
        name = request.POST.get("username")
        #mobile = request.POST.get("mobile")
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
        return redirect("otp",key=key)


class VerifyOtpView(View):
    def get(self, request, key):
        # Render the OTP verification form
        return render(request, "otp.html", {'key': key})

    def post(self, request, key):
        receivedotp = request.POST.get("otp")

        #email = request.POST.get("email")

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


def homePage(request):
    return render(request, 'homePage.html')
