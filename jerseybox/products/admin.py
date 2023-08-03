
# Register your models here.
from django.contrib import admin
from .models import Gender,Continent,Nation,League,Team,Jersey,Product



class GenderAdmin(admin.ModelAdmin):
    list_display = ('name',)


class ContinentAdmin(admin.ModelAdmin):
    list_display = ('name',)

class NationAdmin(admin.ModelAdmin):
    list_display = ('name', 'continent')

class LeagueAdmin(admin.ModelAdmin):
    list_display = ('name', 'nation')

class TeamAdmin(admin.ModelAdmin):
    list_display = ('name', 'league')

class JerseyAdmin(admin.ModelAdmin):
    list_display = ('team', 'jersey_type')

class ProductAdmin(admin.ModelAdmin):
    list_display = ('id','name', 'team', 'actual_price','selling_price','image1','image2')

admin.site.register(Continent, ContinentAdmin)
admin.site.register(Nation, NationAdmin)
admin.site.register(League, LeagueAdmin)
admin.site.register(Team, TeamAdmin)
admin.site.register(Jersey, JerseyAdmin)
admin.site.register(Product, ProductAdmin)
admin.site.register(Gender, GenderAdmin)
