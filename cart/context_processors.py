from .models import Cart, CartItem
from .views import get_cart_id

def cart_counter(request):
    cart_counter = 0

    try:
        if request.user.is_authenticated:
            cart = Cart.objects.filter(user=request.user).first()
        else:
            cart = Cart.objects.filter(cart_id=get_cart_id(request)).first()

        if cart:
            cart_items = CartItem.objects.filter(cart=cart, is_active=True)
            for item in cart_items:
                cart_counter += item.quantity

    except:
        cart_counter = 0

    return dict(cart_counter=cart_counter)
