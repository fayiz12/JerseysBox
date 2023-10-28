from django.urls import path
from . import views



urlpatterns=[
    path('',views.HomeView.as_view(),name='home'),
    path('products/detail/<uuid:product_id>/',views.ProductDetailView.as_view(),name='product_detail'),
    path('league/<uuid:league_id>/', views.LeagueProductsView.as_view(), name='league_products'),
    path('products/<str:gender>/',views.GenderProductsView.as_view(), name='gender_products'),
    path('clubs/<uuid:club_id>/products/', views.ClubProducts.as_view(), name='club_products'),
    path('country/<uuid:country_id>/', views.CountryProducts.as_view(), name='country_products'),
    path('check',views.CheckoutView.as_view(), name='checkout'),
    path('checkout/add_address/', views.AddAddressView.as_view(), name='add_address'),
    # path('checkout/update_address/<uuid:address_id>/', views.UpdateAddressView.as_view(), name='update_address'),
    path('apply-coupon/', views.ApplyCouponView.as_view(), name='apply_coupon'),
    # path('invoice',views.invoice.as_view(),name='invoice')
    path('order_history',views.OrderHistoryView.as_view(),name='order_history'),
    path('invoice/<str:pk>',views.UserInvoice.as_view(),name='invoice'),
    path('track_order/<str:pk>',views.TrackView.as_view(),name='track'),
]
    
