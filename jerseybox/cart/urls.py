
from django.urls import path
from . import views



urlpatterns=[
    # path('add_to_cart/<uuid:product_item_id>/', views.AddToCart.as_view(), name='add_to_cart'),
    
    path('cart/', views.ViewCart.as_view(), name='cart_view'),
    path('add_to_cart/<uuid:pk>/', views.AddToCart.as_view(), name='add_to_cart'),
    path('remove_from_cart/<uuid:product_item_id>/', views.RemoveFromCart.as_view(), name='remove_from_cart'),
   
    # path('add_to_wishlist/<uuid:product_id>/', views.AddToWishlistView.as_view(), name='add_to_wishlist'),
    # path('wishlist/', views.WishlistView.as_view(), name='wishlist_view'),

]
