from django import forms
from .models import Address  
from .models import Order

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




class OrderAdminForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = '__all__'

    def clean(self):
        cleaned_data = super().clean()
        current_status = self.instance.status
        new_status = cleaned_data.get('status')

        if current_status == 'Placed' and new_status != 'Packed':
            raise forms.ValidationError("Cannot change status from Placed to something other than Packed.")
        if current_status == 'Packed' and new_status != 'Shipped':
            raise forms.ValidationError("Cannot change status from Packed to something other than Shipped.")
        if current_status == 'Shipped' and new_status != 'Delivered':
            raise forms.ValidationError("Cannot change status from Shipped to something other than Delivered.")
        if current_status == 'Delivered' and new_status != 'Delivered':
            raise forms.ValidationError("Cannot change status from Delivered to anything")


        return cleaned_data




