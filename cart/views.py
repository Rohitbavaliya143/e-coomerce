from django.shortcuts import render,redirect
from store.models import Product
from cart.models import Cart,CartItem
from django.http import HttpResponse
from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import render,get_object_or_404
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin
# from .utils import get_or_create_cart_id
from .utils import get_cart_id


def get_current_cart(request):
    if request.user.is_authenticated:
        cart, _ = Cart.objects.get_or_create(user=request.user)
    else:
        cart_id = get_cart_id(request)          # your existing function
        cart, _ = Cart.objects.get_or_create(cart_id=cart_id)
    return cart

# def _cart_id(request):
#     cart=request.session.session_key
#     if not cart:
#         cart=request.session.create()
#     return cart

# def add_cart(request, product_id):
#     product = get_object_or_404(Product, id=product_id)

#     if request.user.is_authenticated:
#         cart, _ = Cart.objects.get_or_create(user=request.user)
#     else:
#         cart_id = get_cart_id(request)
#         cart, _ = Cart.objects.get_or_create(cart_id=cart_id)

#     cart_item, created = CartItem.objects.get_or_create(
#         cart=cart,
#         product=product,
#     )
#     if not created:
#         if cart_item.quantity<product.stock:
#             cart_item.quantity += 1
#     else:
#         cart_item.quantity = 1

#     return redirect('cart')


def add_cart(request, product_id):
    product = get_object_or_404(Product, id=product_id)

    # ✅ Get quantity from form
    quantity = int(request.POST.get('quantity', 1))

    # ✅ Get cart
    if request.user.is_authenticated:
        cart, _ = Cart.objects.get_or_create(user=request.user)
    else:
        cart_id = get_cart_id(request)
        cart, _ = Cart.objects.get_or_create(cart_id=cart_id)

    # ✅ Get or create cart item
    cart_item, created = CartItem.objects.get_or_create(
        cart=cart,
        product=product,
    )

    if created:
        # First time adding
        if quantity <= product.stock:
            cart_item.quantity = quantity
    else:
        # Already exists → add selected quantity
        new_quantity = cart_item.quantity + quantity
        if new_quantity <= product.stock:
            cart_item.quantity = new_quantity

    cart_item.save()

    return redirect('cart')



def cart(request):
    cart = None
    cart_items = []
    total = 0
    quantity = 0
    tax = 0
    grand_total = 0

    # 1. Logged-in user → use user cart
    if request.user.is_authenticated:
        cart = Cart.objects.filter(user=request.user).first()
        if not cart:
            # Optional: create empty cart for user
            cart = Cart.objects.create(user=request.user)

    # 2. Guest → use cart_id
    else:
        cart_id = request.session.get('cart_id')
        if cart_id:
            cart = Cart.objects.filter(cart_id=cart_id).first()

    # 3. If we found a cart → load items
    if cart:
        cart_items = cart.items.filter(is_active=True).select_related('product')

        for item in cart_items:
            total += item.sub_total()
            quantity += item.quantity

        tax = (2 * total) / 100
        grand_total = total + tax

    context = {
        'cart_items': cart_items,
        'total': total,
        'quantity': quantity,
        'tax': tax,
        'grand_total': grand_total,
    }

    return render(request, 'store/cart.html', context)











def delete_cart_item(request, product_id):

    product = get_object_or_404(Product, id=product_id)

    # 🔹 Logged in user
    if request.user.is_authenticated:
        cart = Cart.objects.filter(user=request.user).first()

    # 🔹 Guest user
    else:
        cart_id = get_cart_id(request)
        cart = Cart.objects.filter(cart_id=cart_id).first()

    # 🔹 Delete directly (No try/except needed)
    if cart:
        CartItem.objects.filter(product=product, cart=cart).delete()

    return redirect('cart')



def remove_cart(request, product_id):
    product = get_object_or_404(Product, id=product_id)

    if request.user.is_authenticated:
        cart = Cart.objects.filter(user=request.user).first()
    else:
        cart_id = get_cart_id(request)
        cart = Cart.objects.filter(cart_id=cart_id).first()

    if not cart:
        return redirect('cart')

    try:
        cart_item = CartItem.objects.get(product=product, cart=cart)
    except CartItem.DoesNotExist:
        return redirect('cart')

    if cart_item.quantity > 1:
        cart_item.quantity -= 1
        cart_item.save()
    else:
        cart_item.delete()

    return redirect('cart')



class checkoutView(LoginRequiredMixin, View):
    login_url="/login/"
    def get(self,request):
        # cart=Cart.objects.get(cart_id=_cart_id(request))
        cart = get_current_cart(request)
        cart_item=CartItem.objects.filter(cart=cart,is_active=True)
        total=0
        quantity=0
        for item in cart_item:
            total += item.product.price*item.quantity
            quantity += item.quantity
        tax=(2*total)/100
        grand_total = total+tax
        context={
            "cart_items":cart_item,
            "total":total,
            "quantity":quantity,
            "tax":tax,
            "grand_total":grand_total,
        }
        return render(request,"store/checkout.html",context)






