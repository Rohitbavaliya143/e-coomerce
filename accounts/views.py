from django.shortcuts import render,redirect
from .models import Account
from django.contrib import messages
from django.http import HttpResponse
from django.contrib.auth import logout
from django.contrib.auth import authenticate,login as auth_login
from .forms import RegistrationForm
from cart.models import Cart,CartItem
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

# def login_view(request):
#     if request.method == 'POST':
#         email = request.POST['email']
#         password = request.POST['password']
#         user = authenticate(request,email=email,password=password)
#         if user:
#                 auth_login(request,user)

#                 # -------- MERGE SESSION CART INTO DB --------
#                 session_cart = request.session.get('cart')

#                 cart, created = Cart.objects.get_or_create(user=user)

#                 if session_cart:
#                     for pid, item in session_cart.items():
#                         CartItem.objects.update_or_create(
#                             cart=cart,
#                             product_id=pid,
#                             defaults={'quantity': item['quantity']}
#                         )
#                     del request.session['cart']

#                 # -------- LOAD DB CART BACK INTO SESSION --------
#                 db_items = CartItem.objects.filter(cart=cart)
#                 request.session['cart'] = {}

#                 for item in db_items:
#                     request.session['cart'][str(item.product.id)] = {
#                         'quantity': item.quantity,
#                         'price': float(item.product.price)
#                     }

#                 return redirect('home')

#         else:
#             messages.error(request,"Invalid login credentials")

#     return render(request,'accounts/login.html')

def login_view(request):
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']
        user = authenticate(request, email=email, password=password)
        
        if user is not None:
            auth_login(request, user)

            # ─── MERGE GUEST CART AFTER LOGIN ───
            cart_id = request.session.get('cart_id')
            if cart_id:
                try:
                    guest_cart = Cart.objects.get(cart_id=cart_id, user__isnull=True)
                    
                    # Get or create user cart
                    user_cart, _ = Cart.objects.get_or_create(user=user)
                    
                    # Merge items
                    for guest_item in guest_cart.items.all():
                        existing = CartItem.objects.filter(
                            cart=user_cart,
                            product=guest_item.product
                        ).first()
                        
                        if existing:
                            existing.quantity += guest_item.quantity
                            existing.save()
                        else:
                            guest_item.cart = user_cart
                            guest_item.save()
                    
                    # Clean up
                    guest_cart.delete()
                    del request.session['cart_id']
                    
                    messages.success(request, "Your previous cart items are now in your account!")
                
                except Cart.DoesNotExist:
                    pass

            return redirect('home')
        
        else:
            messages.error(request, "Invalid login credentials")

    return render(request, 'accounts/login.html')
def logout(request):
    logout(request)
    return redirect('home')

