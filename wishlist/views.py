from django.shortcuts import render,redirect,get_object_or_404
from .models import Wishlist
from store.models import Product
from django.contrib.auth.decorators import login_required


@login_required
def wishlist(request):
    items = Wishlist.objects.filter(user=request.user)
    return render(request,'wishlist.html',{'items':items})

@login_required(login_url='login')
def add_wishlist(request, product_id):

    product = get_object_or_404(Product, id=product_id)

    item_exists = Wishlist.objects.filter(
        user=request.user,
        product=product
    ).exists()

    if not item_exists:
        Wishlist.objects.create(
            user=request.user,
            product=product
        )

    return redirect('wishlist')


@login_required
def remove_wishlist(request,item_id):

    item = get_object_or_404(
        Wishlist,
        id=item_id,
        user=request.user
    )

    item.delete()
    return redirect('wishlist')