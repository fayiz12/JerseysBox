from django.urls import path
from . import views


urlpatterns=[
    path('products/<int:product_id>/', views.product_list, name='product_detail'),

]