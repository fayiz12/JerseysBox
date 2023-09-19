import hashlib
from django.http import Http404
from django.shortcuts import redirect, render, get_object_or_404
from django.urls import reverse

from .models import UserProfile
from django.contrib import messages
from django.contrib.auth import authenticate, login as auth_login, logout
from .email import *
from django.core.cache import cache
from products.models import *
from django.views import View
import random
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode

from cart.models import *





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
            messages.warning(request, "You are already registered. Please login.")
            return redirect("register")

        if pass1 != pass2:
            messages.warning(request, "Password does not match.")
            return redirect("register")

        otp = str(random.randint(100000, 999999))
        send_otp_email(email, name, otp)
        key = hashlib.sha256(email.encode()).hexdigest()
        cache.set(
            key,
            {"email": email, "name": name, "password": pass1, "otp": otp},
            timeout=600,
        )
        return redirect("otp", key=key)


class VerifyOtpView(View):
    def get(self, request, key):
        # Render the OTP verification form
        return render(request, "otp.html", {"key": key})

    def post(self, request, key):
        receivedotp = request.POST.get("otp")

        signup_data = cache.get(key)
        print(signup_data)
        if not signup_data:
            messages.warning(request, "OTP expired or invalid")
            return redirect("otp", key=key)
        otp = signup_data.get("otp")
        name = signup_data.get("name")
        email = signup_data.get("email")
        password = signup_data.get("password")
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
            email = signup_data.get("email")
            name = signup_data.get("name")
            otp = str(random.randint(100000, 999999))
            print(otp)
            send_otp_email(email, name, otp)
            signup_data["otp"] = otp
            existing_timeout = signup_data.get("timeout", None)
            cache.set(key, signup_data, timeout=existing_timeout)
            return redirect("otp", key=key)
        return redirect("signup")


class ForgotPassword(View):
    def get(self, request):
        return render(request, "password_forgot_form.html")

    def post(self, request):
        email = request.POST.get("email")
        try:
            user = UserProfile.objects.get(email=email)
        except:
            messages.warning(request, "You are not registerd, Please sign up")
            return redirect("register")
        encrypt_id = urlsafe_base64_encode(str(user.email).encode())
        reset_link = f"{request.scheme}://{request.get_host()}{reverse('reset', args=[encrypt_id])}"
        print(reset_link)
        cache_key = f"reset_link_{encrypt_id}"
        cache.set(cache_key, {"reset_link": reset_link}, timeout=20)
        reset_password_email(email, reset_link)
        messages.success(request, "Password reset link sent to your email.")
        return redirect("login")


class UserResetPassword(View):
    def get(self, request, encrypt_id):
        cache_key = f"reset_link_{encrypt_id}"
        cache_data = cache.get(cache_key)
        if not cache_data:
            raise Http404("Reset link has expired")
        reset_id = cache_data.get("reset_link")
        return render(request, "password_reset.html", {"reset": reset_id})

    def post(self, request, encrypt_id):
        cache_key = f"reset_link_{encrypt_id}"
        email = str(urlsafe_base64_decode(encrypt_id), "utf-8")
        user = UserProfile.objects.get(email=email)
        new_password = request.POST.get("pass1")
        user.set_password(new_password)
        user.save()
        cache.delete(cache_key)
        messages.success(
            request,
            "Password reset successful. You can now log in with your new password.",
        )
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


class UserSignout(View):
    def get(self, request):
        logout(request)
        return redirect("login")







