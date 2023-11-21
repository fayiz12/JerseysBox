

from django.shortcuts import redirect
from django.views import View
from django.contrib import messages
from .models import *
from django.shortcuts import get_object_or_404



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


class OrderCancellationView(View):
    def get(self, request, order_id):
        try:
            order = Order.objects.get(id=order_id, user=request.user)

            if order.status in ['Placed', 'Packed','Pending']:
    
                order.status = 'Cancelled'
                order.save()
                messages.success(request, 'Order has been cancelled successfully.')
            else:
                messages.error(request, 'This order cannot be cancelled.')

        except Order.DoesNotExist:
            messages.error(request, 'Order not found or you do not have permission to cancel it.')

        return redirect('order_history')


class SubmitReviewView(View):
    def post(self, request, product_id):
        product = get_object_or_404(Product, id=product_id)
        user = request.user

        # Check if the user has ordered the product
        user_has_ordered_product = OrderItem.objects.filter(order__user=user, product__product_id=product).exists()


        if not user_has_ordered_product:
            messages.error(request, 'You must order this product to leave a review.')
        else:
            existing_review = Review.objects.filter(user=user, product=product).exists()
            if existing_review:
                messages.error(request, 'You can only add one review per product.')
            else:
                content = request.POST.get('review')
                rating = request.POST.get('rating')  # Get the selected rating from the form
                review = Review.objects.create(user=user,product=product, description=content, rating=rating)
                review.save()
                messages.success(request, 'Review added successfully.')

        return redirect('product_detail', product_id=product_id)