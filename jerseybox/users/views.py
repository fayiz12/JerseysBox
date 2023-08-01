from django.shortcuts import redirect, render,HttpResponse
from django.contrib.auth.forms import UserCreationForm
from .models import UserProfile,UserProfileManager
from django.contrib import messages
from django.contrib.auth import authenticate,login as auth_login
from .email import send_otp_email
from django.core.cache import cache





def home(request):
    return render(request,'users/product.html')

def signup(request):
    if request.method=='POST':
        email=request.POST.get('email')
        name=request.POST.get('username')
        mobile=request.POST.get('mobile')
        pass1=request.POST.get('pass1')
        pass2=request.POST.get('pass2')
        print(email,name,mobile,pass1)
        
        userobj=UserProfile.objects.filter(email=email)
        if userobj.exists():
            messages.warning(request,'You are already registerd,Please login')
            return redirect(signup)
        if pass1!=pass2:
            messages.warning(request,'password does not match')
            return redirect(signup)
        send_otp_email(email,name,mobile,pass1)
        return redirect(verify_otp)

    return render(request,'users/signup.html')



def verify_otp(request):
    if request.method=='POST':
        receivedotp=request.POST.get('otp')
        try:
            signup_data=cache.get('cache_data')
            otp=signup_data['otp']
            name=signup_data['name']
            mobile=signup_data['mobile']
            email=signup_data['email']
            password=signup_data['password']
        except:
            messages.warning(request,'OTP has Expired')
            return redirect(verify_otp)
        print(name,mobile,email,password)
        print(otp,receivedotp)
        if receivedotp!=otp:
            messages.warning(request,'OTP mismatch')
            return redirect(verify_otp)
        UserProfile.objects.create_user(username=name,email=email,mobile=mobile,password=password)
        return redirect(login)
    return render(request,'users/otp.html')



def login(request):
    if request.method=='POST':
        name = request.POST.get('username')  
        pass1 = request.POST.get('pass1')

        user=authenticate(request,username=name,password=pass1)
        if user is not None:
            print(name)
            auth_login(request,user)
            
            
            return redirect('home')
        else:
            
            return redirect("login")

    return render(request,"users/login.html")


