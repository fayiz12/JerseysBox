from django.urls import path
from . import views



urlpatterns=[
    path('register',views.signup,name='register'),
    path('login',views.login,name='login'),
    path('verify',views.verify_otp,name='otp'),
    path('',views.home,name='home'),

]