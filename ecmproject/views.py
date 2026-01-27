from django.shortcuts import render
from store.models import Product
def home(request):
    products =  Product.objects.all().filter(is_available=True)
    context = { 
        'products':products,
        }
    return render(request,'index.html',context)
def product_detail(request,product_id):
    Product_details=Product.objects.all().filter(is_available=True)
    context={
        'product_detail':Product_details,
             }
    return render(request,'product-detail.html',context)
def about(request):
    return render(request,'about.html')
def contact(request):
    return render(request,'contact.html')
def services(request):
    return render(request,'services.html')
