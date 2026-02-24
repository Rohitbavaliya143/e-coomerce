from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.db import transaction # For atomic transactions
from .forms import OrderForm
from .models import Order, OrderProduct
from cart.models import CartItem 
from store.models import Product
from django.contrib.auth.decorators import login_required


@login_required(login_url='login')
def checkout(request):
    # 1. Get Cart Items
    cart_items = CartItem.objects.filter(user=request.user)
    cart_count = cart_items.count()
    
    if cart_count <= 0:
        return redirect('store')

    # 2. Calculate Prices (Server-side calculation is safer)
    total_price = 0
    shipping_fee = 10.00 # Example fixed shipping
    
    for item in cart_items:
        total_price += (item.product.price * item.quantity)
    
    grand_total = total_price + shipping_fee

    if request.method == 'POST':
        form = OrderForm(request.POST)
        if form.is_valid():
            # --- START ATOMIC TRANSACTION ---
            with transaction.atomic():
                # 3. Save Order Data
                order = form.save(commit=False)
                order.user = request.user
                order.total_price = grand_total
                order.payment_method = request.POST.get('payment_method', 'COD')
                order.save()

                # 4. Move Cart Items to Order Products & Update Stock
                for item in cart_items:
                    order_product = OrderProduct()
                    order_product.order_id = order.id
                    order_product.product_id = item.product_id
                    order_product.quantity = item.quantity
                    order_product.product_price = item.product.price
                    order_product.ordered = True
                    order_product.save()

                    # Reduce stock
                    product = Product.objects.get(id=item.product_id)
                    product.stock -= item.quantity
                    product.save()

                # 5. Clear Cart
                cart_items.delete()

                # 6. Handle Payment Logic
                if order.payment_method == 'COD':
                    return redirect('order_complete') # Redirect to success page
                
                # Add Online Payment Logic here (e.g., Stripe/PayPal)
                
            # --- END ATOMIC TRANSACTION ---
    else:
        form = OrderForm()

    context = {
        'form': form,
        'cart_items': cart_items,
        'total_price': total_price,
        'shipping_fee': shipping_fee,
        'grand_total': grand_total,
    }
    return render(request, 'checkout.html', context)

def order_complete(request, order_number):
    order = get_object_or_404(Order, order_number=order_number)
    ordered_products = OrderProduct.objects.filter(order=order)
    context = {
        'order': order,
        'ordered_products': ordered_products,
        'subtotal': order.total_price,
        'tax': order.tax,
        'grand_total': order.total_price,
    }
    return render(request, 'store/order_complete.html', context)
@login_required
def order_detail(request, order_number):
    order = get_object_or_404(Order, order_number=order_number, user=request.user)
    ordered_products = OrderProduct.objects.filter(order=order)

    context = {
        'order': order,
        'ordered_products': ordered_products,
        'subtotal': order.total_price,
        'tax': order.tax,
        'grand_total': order.total_price
    }

    return render(request, 'store/order_detail.html', context)