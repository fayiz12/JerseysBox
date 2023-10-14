from django.contrib import admin
from .models import UserProfile
from unfold.admin import ModelAdmin



# Register your models here.


class UserAdmin(ModelAdmin):
    list_display=['id','username','email','is_active','is_superuser']
    search_fields=['email','username']
    readonly_fields=['last_login','password']
    list_filter=['last_login']
    




admin.site.register(UserProfile,UserAdmin)


