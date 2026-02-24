# import uuid
# from .models import Cart
# def get_or_create_cart_id(request):
#     if 'cart_id' not in request.session:
#         request.session['cart_id'] = str(uuid.uuid4())
#     return request.session['cart_id']





import uuid

def get_cart_id(request):
    if 'cart_id' not in request.session:
        request.session['cart_id'] = str(uuid.uuid4())
    return request.session['cart_id']