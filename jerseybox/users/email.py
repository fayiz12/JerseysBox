import random
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.conf import settings
from django.core.cache import cache


def send_otp_email(email,name,mobile,password):
    subject='Account verification OTP'
    otp=str(random.randint(100000,999999))
    html_content=render_to_string('users/emailOTP.html',{'username':name,'otp':otp})
    send_mail(subject,'',settings.EMAIL_HOST_USER,[email],html_message=html_content)
    cache.set('cache_data',{'email':email,'name':name,'password':password,'mobile':mobile,'otp':otp},timeout=60)