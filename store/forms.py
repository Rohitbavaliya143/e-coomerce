from django import forms
from order.models import Order


STATE_CHOICES = [
    ('', 'Choose State'),
    ('Gujarat', 'Gujarat'),
    ('Maharashtra', 'Maharashtra'),
    ('Rajasthan', 'Rajasthan'),
    ('Delhi', 'Delhi'),
]



class OrderForm(forms.ModelForm):

    state = forms.ChoiceField(
        choices=STATE_CHOICES,
        widget=forms.Select(attrs={
            'class': 'form-select'
        })
    )

    def clean_phone(self):
        phone = self.cleaned_data.get('phone')

        if not phone.isdigit():
            raise forms.ValidationError("Phone number must contain only digits")

        if len(phone) != 10:
            raise forms.ValidationError("Phone number must be 10 digits")

        return phone
    

    def clean_pincode(self):
        pincode = self.cleaned_data.get('pincode')

        if not pincode.isdigit():
            raise forms.ValidationError("Pincode must contain only digits")

        if len(pincode) != 6:
            raise forms.ValidationError("Pincode must be 6 digits")

        return pincode
    

    def clean_state(self):
        state = self.cleaned_data.get('state')

        if state == '':
            raise forms.ValidationError("Please select a state")

        return state
    

    def clean_email(self):
        email = self.cleaned_data.get('email')

        if "@" not in email:
            raise forms.ValidationError("Enter valid email")

        return email
    
    
    class Meta:
        model = Order
        fields = ['first_name', 'last_name', 'phone', 'email', 'address', 'city', 'state', 'pincode']
        
        # This adds the "form-control" class automatically to all inputs
        # so they look nice and modern with Bootstrap
        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'John'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Doe'}),
            'phone': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '+1 234 567 89'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'john.doe@example.com'}),
            'address': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '123 Main St'}),
            'city': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'New York'}),
            'state': forms.Select(attrs={'class': 'form-select'}),
            'pincode': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '10001'}),
        }