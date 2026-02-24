from django.shortcuts import render,redirect
from store.models import Product
from order.models import Order,OrderProduct
from category.models import category
from cart.models import CartItem
from django.shortcuts import render,get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import View
from cart.views import get_current_cart
from .forms import OrderForm
from django.db import transaction

def store(request,category_slug=None):
    categories=None
    products=None
    if category_slug != None:
        categories=get_object_or_404(category,slug=category_slug)
        products=Product.objects.filter(category=categories,is_available=True)
        products_count=products.count()
    else:
        products=Product.objects.all().filter(is_available=True)
    context = {
        'products':products,
    }
    return render(request,'store/store.html',context)
def products_by_audience(request, audience):
    products = Product.objects.filter(
        audience=audience,
        is_available=True
    )
    return render(request, 'store/store.html', {
        'products': products,
        'selected_audience': audience,
        'products':products,
    })
# def product_store(request):
#     product=Product.objects.filter(
#         is_available=True,
#         )
#     context={
#         'products':product
#         }
#     return render(request,'product-detail.html',context)
# Create your views here.
def product_detail(request, category_slug,product_slug):
    # product = get_object_or_404(Product, id=product_id, is_available=True)
    # context = {
    #     'product': product,
    # }
    try:
        single_product=Product.objects.get(category__slug=category_slug,slug=product_slug)
    except Exception as e:
        raise
    context={
        'single_product':single_product,
    }
    return render(request, 'product-detail.html',context)   # ← use namespaced template





class CheckoutView(LoginRequiredMixin, View):
    login_url = '/login/'

    def get(self, request):

        cart = get_current_cart(request)
        cart_items = CartItem.objects.filter(cart=cart, is_active=True)

        if not cart_items.exists():
            return redirect('cart')

        total = 0
        quantity = 0

        for item in cart_items:
            total += item.product.price * item.quantity
            quantity += item.quantity

        tax = (2 * total) / 100
        grand_total = total + tax

        form = OrderForm()

        context = {
            'form': form,
            'cart_items': cart_items,
            'total': total,
            'quantity': quantity,
            'tax': tax,
            'grand_total': grand_total,
        }

        return render(request, 'store/checkout.html', context)


    def post(self, request):

        cart = get_current_cart(request)
        cart_items = CartItem.objects.filter(cart=cart, is_active=True)

        if not cart_items.exists():
            return redirect('cart')

        total = 0
        for item in cart_items:
            total += item.product.price * item.quantity

        TAX_PERCENTAGE = 2
        tax = (total * TAX_PERCENTAGE) / 100
        shipping_fee = 10
        grand_total = total + tax

        form = OrderForm(request.POST)

        if form.is_valid():
            with transaction.atomic():

                # 1️⃣ Save Order
                order = form.save(commit=False)
                order.user = request.user
                order.total_price = grand_total
                order.tax=tax
                order.payment_method = request.POST.get('payment_method', 'COD')
                order.save()

                # 2️⃣ Move Cart Items to OrderProduct
                for item in cart_items:

                    OrderProduct.objects.create(
                        order=order,
                        product=item.product,
                        quantity=item.quantity,
                        product_price=item.product.price,
                        ordered=True
                    )

                    # Reduce stock
                    product = item.product
                    product.stock -= item.quantity
                    product.save()

                # 3️⃣ Clear Cart
                cart_items.delete()

                # 4️⃣ Payment Logic
                if order.payment_method == 'COD':
                    return redirect('order_complete', order_number=order.order_number)

                # 👉 Here you can integrate Stripe / Razorpay later

        # If form invalid
        context = {
            'form': form,
            'cart_items': cart_items,
            'grand_total': grand_total,
        }

        return render(request, 'store/checkout.html', context)