from django import template

register = template.Library()

@register.filter(name='rating_stars')  
def rating_stars(value):
    # Convert the numeric rating to a string of star icons
    full_stars = int(value)
    half_stars = 1 if (value - full_stars) >= 0.5 else 0
    empty_stars = 5 - full_stars - half_stars

    return "★" * full_stars + "½" * half_stars + "☆" * empty_stars
