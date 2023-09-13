from django.urls import path
from . import views



urlpatterns=[
    
    
    path('wishlist/', views.WishlistView.as_view(), name='wishlist_view'),
    path('add_to_wishlist/<uuid:product_id>/', views.AddToWishlistView.as_view(), name='add_to_wishlist'),
    path('remove_from_wishlist/<uuid:product_id>/', views.RemoveFromWishlistView.as_view(), name='remove_from_wishlist'),
]