from django.urls import path
from . import views



urlpatterns=[
    path('',views.HomeView.as_view(),name='home'),
    path('products/detail/<uuid:product_id>/',views.ProductDetailView.as_view(),name='product_detail'),
    path('league/<uuid:league_id>/', views.LeagueProductsView.as_view(), name='league_products'),
    path('products/<str:gender>/',views.GenderProductsView.as_view(), name='gender_products'),
    path('clubs/<uuid:club_id>/products/', views.ClubProducts.as_view(), name='club_products'),
    path('country/<uuid:country_id>/', views.CountryProducts.as_view(), name='country_products'),
    
]