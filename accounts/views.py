from django.shortcuts import render,redirect,get_object_or_404
from .models import Account
from django.contrib import messages
from django.http import HttpResponse
from django.contrib.auth import logout
from django.contrib.auth import authenticate,login as auth_login
from django.contrib.auth.decorators import login_required
from .forms import ContactForm
from .forms import RegistrationForm
from cart.models import Cart,CartItem
import uuid
from .forms import EditProfileForm
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth import update_session_auth_hash
from order.models import Order

def register(request):

    if request.method == "POST":
        form = RegistrationForm(request.POST)

        if form.is_valid():
            user = form.save(commit=False)

            user.set_password(form.cleaned_data['password'])
            user.is_active = True
            user.save()

            messages.success(request, "Account created successfully")

            # redirect to login page
            return redirect('login')

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


def contact(request):

    if request.method == "POST":

        form = ContactForm(request.POST)

        if form.is_valid():

            form.save()

            messages.success(request,"✅ Your message has been sent successfully!")

            return redirect('contact')

        else:
            messages.error(request,"❌ Please correct the errors below.")

    else:
        form = ContactForm()

    return render(request,'contact.html',{'form':form})

@login_required
def dashboard(request):
    return render(request,'accounts/dashboard.html')

@login_required
def edit_profile(request):

    if request.method == "POST":

        form = EditProfileForm(request.POST,instance=request.user)

        if form.is_valid():

            form.save()

            messages.success(request,"Profile updated successfully")

            return redirect('dashboard')

    else:

        form = EditProfileForm(instance=request.user)

    return render(request,'accounts/edit_profile.html',{'form':form})

@login_required
def change_password(request):

    if request.method == "POST":

        form = PasswordChangeForm(request.user,request.POST)

        if form.is_valid():

            user = form.save()

            update_session_auth_hash(request,user)

            messages.success(request,"Password changed successfully")

            return redirect('dashboard')

    else:

        form = PasswordChangeForm(request.user)

    return render(request,'accounts/change_password.html',{'form':form})



@login_required
def my_orders(request):

    orders = Order.objects.filter(user=request.user).order_by('-created_at')

    return render(request,'accounts/my_orders.html',{'orders':orders})



@login_required
def order_detail(request,order_id):

    order = get_object_or_404(Order,id=order_id,user=request.user)

    return render(request,'accounts/order_detail.html',{'order':order})