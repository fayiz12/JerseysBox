

from django.shortcuts import redirect
from django.views import View
from .models import Review, ReviewImage, Product

class UserReview(View):
    def post(self, request, pk):
        rating = request.POST.get('rating')
        title = request.POST.get('title')
        description = request.POST.get('description')
        images = request.FILES.getlist('images')
        
        try:
            product = Product.objects.get(id=pk)
        except Product.DoesNotExist:
            # Handle the case where the product doesn't exist
            return redirect('product_not_found')  # Replace 'product_not_found' with your actual URL name
            
        # Update or create a review for the current user and product
        review, created = Review.objects.update_or_create(
            user=request.user,
            product=product,
            defaults={'rating': rating, 'title': title, 'description': description}
        )
        
        # Handle the case where review creation fails
        if not created and (rating or title or description):
            # Update the review if any of the fields are provided
            review.rating = rating
            review.title = title
            review.description = description
            review.save()
        
        if images:
            # Create ReviewImage objects for uploaded images
            for image in images:
                ReviewImage.objects.create(image=image, review=review)
        
        return redirect(request.META.get('HTTP_REFERER'))
