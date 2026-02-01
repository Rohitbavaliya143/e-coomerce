from django.shortcuts import render,redirect
from .models import Account
from django.contrib import messages
from django.contrib.auth import authenticate,login as auth_login
from .forms import RegistrationForm
import uuid


def register(request):
    if request.method == "POST":
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password'])
            user.is_active = True
            user.save()
            messages.success(request, "Account created successfully")
            # return redirect('login')
        else:
            messages.error(request, "Please correct the errors below.")
    else:
        form = RegistrationForm()

    return render(request, 'accounts/register.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']
        user = authenticate(request,email=email,password=password)
        if user:
            auth_login(request,user)
            return redirect('home')
        else:
            messages.error(request,"Invalid login credentials")
    return render(request,'accounts/login.html')