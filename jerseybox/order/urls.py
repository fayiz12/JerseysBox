from django.urls import path
from .views import UserReview

urlpatterns = [
    
    path('review/<uuid:review_id>/', UserReview.as_view(), name='reviews'),
]
