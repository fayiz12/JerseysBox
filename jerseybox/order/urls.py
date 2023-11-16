from django.urls import path
from .views import *

urlpatterns = [
    
    path('review/<uuid:review_id>/', UserReview.as_view(), name='reviews'),
    path('order/cancel/<uuid:order_id>/', OrderCancellationView.as_view(), name='order_cancel'),
    path('submit_review/<uuid:product_id>/',SubmitReviewView.as_view(), name='submit_review'),

]
