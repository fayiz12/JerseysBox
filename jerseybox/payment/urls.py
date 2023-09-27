
from django.urls import path
from .views import PaymentView

urlpatterns = [
    
    path('payment/<uuid:order_id>/', PaymentView.as_view(), name='payment'),
]
