from django.urls import path
from . import views



urlpatterns=[
    path('user_registration',views.SignupView.as_view(),name='register'),
    path('login',views.LoginView.as_view(),name='login'),
    path('verify',views.VerifyOtpView.as_view(),name='otp'),
    path('',views.HomeView.as_view(),name='home'),
    path('single/<int:id>/',views.ProductDetailView.as_view(),name='detail'),

]