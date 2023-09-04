from django.contrib import admin
from .models import *
from django.utils.safestring import mark_safe


class ContinentAdmin(admin.ModelAdmin):
    list_display = ('name', 'code',)


class CountryModelAdmin(admin.ModelAdmin):
    list_display = ('id','country', 'continent', 'display_country_flag', )
    list_filter = ('continent',)
    list_per_page = 20
    search_fields = ('country',)

    def display_country_flag(self, obj):
        return mark_safe(f'<img src="{obj.flag_image_path}" alt="{obj.country.name} flag" width="30">')

    display_country_flag.short_description = 'Flag'


class LeagueAdmin(admin.ModelAdmin):
    list_display = ('name', 'display_logo',)  # Use 'display_logo' here

    def display_logo(self, obj):  # Define the method as 'display_logo'
        return mark_safe(f'<img src="{obj.logo.url}" alt="{obj.name} logo" style="max-width: 50px; max-height: 50px;">')

    display_logo.short_description = 'Logo'


class ClubAdmin(admin.ModelAdmin):
    list_display = ('name', 'league', 'club_logo',)
    list_filter = ('league',)

    def club_logo(self, obj):
        return mark_safe(f'<img src="{obj.logo.url}" alt="{obj.name} logo" width="30">')


admin.site.register(Continent, ContinentAdmin)
admin.site.register(CountryModel, CountryModelAdmin)
admin.site.register(League, LeagueAdmin)
admin.site.register(Club, ClubAdmin)
