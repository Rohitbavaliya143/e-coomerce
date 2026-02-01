from .models import Cart,CartItem
from .views import _cart_id
def cart_counter(request):
    cart_counter=0
    try:
        cart=Cart.objects.get(cart_id=_cart_id(request))
        cart_item=CartItem.objects.filter(cart=cart,is_active=True)
        for item in cart_item:
            cart_counter += item.quantity
    except:
        pass
    return dict(cart_counter=cart_counter) 