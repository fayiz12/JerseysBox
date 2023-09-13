from django.contrib import admin
from .models import *
# Register your models here.


class WishlistAdmin(admin.ModelAdmin):
    list_display = ('id',)



admin.site.register(WishlistModel, WishlistAdmin)
