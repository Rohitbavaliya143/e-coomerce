from django.shortcuts import render
def home(request):
    return render(request,'index.html')
def product_detail(request):
    return render(request,'product-detail.html')