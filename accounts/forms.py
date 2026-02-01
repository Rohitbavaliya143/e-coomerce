from django import forms
from .models import Account
import uuid
class RegistrationForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': '••••••••'}))
    confirm_password = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': '••••••••'}))

    class Meta:
        model = Account
        fields = ['first_name', 'last_name', 'email', 'phone_number']
        widgets = {
            'first_name': forms.TextInput(attrs={'placeholder': 'Atul'}),
            'last_name': forms.TextInput(attrs={'placeholder': 'Kumar'}),
            'email': forms.EmailInput(attrs={'placeholder': 'atul@example.com'}),
            'phone_number': forms.TextInput(attrs={'placeholder': '9876543210'}),
        }

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get('password')
        confirm = cleaned_data.get('confirm_password')

        if password and confirm and password != confirm:
            raise forms.ValidationError("Passwords do not match")
        return cleaned_data
    def save(self, commit = True):
        user=super().save(commit=False)
        base=user.email.split('@')[0]
        user.username = base + "_" + uuid.uuid4().hex[:6]
        if commit:
            user.save()
        return user

