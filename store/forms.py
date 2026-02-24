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