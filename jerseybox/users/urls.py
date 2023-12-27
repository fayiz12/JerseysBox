from django.urls import path
from . import views



urlpatterns=[
    path('user_registration/',views.SignupView.as_view(),name='register'),
    path('login/',views.LoginView.as_view(),name='login'),
    path('verify/<str:key>/',views.VerifyOtpView.as_view(),name='otp'),
    path('resend_otp/<str:key>/', views.ResendOTP.as_view(), name='resend_otp'),
    path('forgot_password/', views.ForgotPassword.as_view(), name='forgot'),
    path('rreset_password/<str:encrypt_id>/',views.UserResetPassword.as_view(),name='reset'),
    path('signout/',views.UserSignout.as_view(),name='signout'),
    path('user_profile/',views.UserProfileView.as_view(),name='userprofile'),
    path('user_address/',views.AllAddressView.as_view(),name='address'),
]