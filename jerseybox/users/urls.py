from django.urls import path
from . import views



urlpatterns=[
    path('user_registration/',views.SignupView.as_view(),name='register'),
    path('login/',views.LoginView.as_view(),name='login'),
    path('verify/<str:key>/',views.VerifyOtpView.as_view(),name='otp'),
    path('',views.HomeView.as_view(),name='home'),
    path('products/detail/<uuid:product_id>/',views.ProductDetailView.as_view(),name='product_detail'),
    
    path('resend_otp/<str:key>/', views.ResendOTP.as_view(), name='resend_otp'),
    path('forgot_password/', views.ForgotPassword.as_view(), name='forgot'),
    path('rreset_password/<str:encrypt_id>/',views.UserResetPassword.as_view(),name='reset'),
    path('signout/',views.UserSignout.as_view(),name='signout'),
    path('league/<uuid:league_id>/', views.LeagueProductsView.as_view(), name='league_products'),
    path('products/<str:gender>/',views.GenderProductsView.as_view(), name='gender_products'),
    path('clubs/<uuid:club_id>/products/', views.club_products.as_view(), name='club_products'),
    path('country/<uuid:country_id>/', views.country_products.as_view(), name='country_products'),
]