from django import forms
from .models import Address  

class AddressForm(forms.ModelForm):
    class Meta:
        model = Address
        fields = ['name', 'phone_number', 'street_address', 'city', 'postal_code', 'state', 'country']


class OrderForm(forms.Form):
    PAYMENT_CHOICES = [('cash_on_delivery', 'Cash on Delivery'), ('razorpay', 'Razorpay')]
    
    # Set custom id for "Cash on Delivery" radio button
    payment_method_cod = forms.ChoiceField(
        label='Payment Method',
        choices=PAYMENT_CHOICES,
        widget=forms.RadioSelect(attrs={'id': 'custom_cod_id'}),
        initial='cash_on_delivery',  # Set initial value if needed
    )
    
    # Set custom id for "Razorpay" radio button
    payment_method_razorpay = forms.ChoiceField(
        choices=PAYMENT_CHOICES,
        widget=forms.RadioSelect(attrs={'id': 'custom_razorpay_id'}),
        initial='razorpay',  # Set initial value if needed
    )





