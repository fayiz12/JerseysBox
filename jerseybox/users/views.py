from django.shortcuts import render,HttpResponse
from django.contrib.auth.forms import UserCreationForm
from .models import UserProfile





def home(request):
    pass

def signup(request):
    if request.method=='POST':
        email=request.POST.get('email')
        name=request.POST.get('username')
        mobile=request.POST.get('mobile')
        pass1=request.POST.get('pass1')
        pass2=request.POST.get('pass2')
        if pass1==pass2:
            
            my_user=UserProfile.objects.create_user(email,name,mobile,pass1)
            my_user.save()
            print(email,name,mobile,pass1)
            

        

    return render(request,'users/signup.html')


def login(request):
    return render(request,"users/login.html")