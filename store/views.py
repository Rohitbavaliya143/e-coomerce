from django.shortcuts import render
from store.models import Product
from category.models import category
from django.shortcuts import render,get_object_or_404
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
