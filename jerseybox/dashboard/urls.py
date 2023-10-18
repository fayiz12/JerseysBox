from django.urls import path
from .views import *

urlpatterns = [
    
    path('ab',DashboardView.as_view(), name='dashboard'),
]
