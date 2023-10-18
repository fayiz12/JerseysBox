from django.shortcuts import render
from users.models import UserProfile  # Make sure you import your custom user model
from django.views import View

class DashboardView(View):
    def get(self, request):
        total_user = UserProfile.objects.count()
        return render(request, 'admin/index.html', {'total_user': total_user})
