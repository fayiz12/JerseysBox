from django import forms
from .models import Address  

class AddressForm(forms.ModelForm):
    class Meta:
        model = Address
        fields = ['name', 'phone_number', 'street_address', 'city', 'postal_code', 'state', 'country']