from django import forms
from .models import Account
from .models import Contact
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


    # Email already exists validation
    def clean_email(self):
        email = self.cleaned_data.get('email')

        if Account.objects.filter(email=email).exists():
            raise forms.ValidationError("Email already exists")

        return email


    # Phone number validation
    def clean_phone_number(self):
        phone = self.cleaned_data.get('phone_number')

        if len(phone) != 10 or not phone.isdigit():
            raise forms.ValidationError("Enter valid 10 digit phone number")

        return phone


    # Save user
    def save(self, commit=True):
        user = super().save(commit=False)

        base = user.email.split('@')[0]
        user.username = base + "_" + uuid.uuid4().hex[:6]

        user.set_password(self.cleaned_data['password'])  # password hashing

        if commit:
            user.save()

        return user
class ContactForm(forms.ModelForm):

    class Meta:
        model = Contact
        fields = ['name','email','subject','message']

        widgets = {
            'name': forms.TextInput(attrs={
                'class':'form-control',
                'placeholder':'Enter your name'
            }),

            'email': forms.EmailInput(attrs={
                'class':'form-control',
                'placeholder':'Enter your email'
            }),

            'subject': forms.TextInput(attrs={
                'class':'form-control',
                'placeholder':'Subject'
            }),

            'message': forms.Textarea(attrs={
                'class':'form-control',
                'placeholder':'Write your message...',
                'rows':5
            }),
        }




class EditProfileForm(forms.ModelForm):
    class Meta:
        model = Account

        fields = [
            'first_name',
            'last_name',
            'phone_number',
            'email'
        ]

        widgets = {

            'first_name': forms.TextInput(attrs={
                'class':'form-control'
            }),

            'last_name': forms.TextInput(attrs={
                'class':'form-control'
            }),

            'phone_number': forms.TextInput(attrs={
                'class':'form-control'
            }),

            'email': forms.EmailInput(attrs={
                'class':'form-control'
            }),

        }