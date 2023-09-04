from django.urls import path
from . import views

urlpatterns = [
    # Add your other URL patterns here
    path('league/<uuid:league_id>/', views.league_products, name='league_products'),
]