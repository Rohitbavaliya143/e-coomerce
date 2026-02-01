from django.shortcuts import render,redirect
from store.models import Product
from cart.models import Cart,CartItem
from django.http import HttpResponse
from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import render,get_object_or_404

def _cart_id(request):
    cart=request.session.session_key
    if not cart:
        cart=request.session.create()
    return cart
def add_cart(request,product_id):
    product=Product.objects.get(id=product_id)
    try:
        cart=Cart.objects.get(cart_id=_cart_id(request))
    except Cart.DoesNotExist: 
        cart=Cart.objects.create(cart_id=_cart_id(request))
    try:
        cart_item=CartItem.objects.get(product=product,cart=cart)
        cart_item.quantity += 1
        cart_item.save()
    except CartItem.DoesNotExist:
        cart_item=CartItem.objects.create(
            product=product,
            cart=cart,
            quantity=1,
        )
        cart_item.save()  
    # return HttpResponse(cart_item.quantity)
    return redirect('cart')
def cart(request,total=0,quantity=0,cart_item=None):
    try:
        cart=Cart.objects.get(cart_id=_cart_id(request))
        cart_items=CartItem.objects.filter(cart=cart,is_active=True)
        for cart_item in cart_items:
            cart_item.sub_total() 
            total += (cart_item.product.price * cart_item.quantity)
            quantity += cart_item.quantity
        tax=(2*total)/100
        grand_total= total+tax
    except ObjectDoesNotExist:
        pass
    context={
        'total':total,
        'quantity':quantity,
        'cart_items':cart_items,
        'tax':tax,
        'grand_total':grand_total,
    }
    return render(request,'store/cart.html',context)
# def remove_cart(request,product_id):
#     product=Product.objects.get(id=product_id)
#     cart=Cart.objects.get(cart_id=_cart_id(request))
#     if request.user.is_authenticated:
#         cart_item=CartItem.objects.get(
#             product=product,
#             cart=cart,
#         )
#     else:
#         cart=Cart.objects.get(Cart,cart_id=_cart_id(request))
#         cart_item=CartItem.objects.get(
#             product=product,
#             cart=cart,
#         )
#         cart_item.delete()
#         return redirect('cart')


def delete_cart_item(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    cart = get_object_or_404(Cart, cart_id=_cart_id(request))

    try:
        cart_item = CartItem.objects.get(product=product, cart=cart)
        cart_item.delete()
    except CartItem.DoesNotExist:
        pass

    return redirect('cart')

def remove_cart(request, product_id):
    # product લાવ
    product = get_object_or_404(Product, id=product_id)
    
    # cart લાવ (session પરથી)
    cart = get_object_or_404(Cart, cart_id=_cart_id(request))

    try:
        # cart item લાવ
        cart_item = CartItem.objects.get(product=product, cart=cart)
    except CartItem.DoesNotExist:
        # જો item ન હોય તો સીધું cart page
        return redirect('cart')

    # main logic
    if cart_item.quantity > 1:
        cart_item.quantity -= 1
        cart_item.save()
    else:
        cart_item.delete()

    return redirect('cart')

