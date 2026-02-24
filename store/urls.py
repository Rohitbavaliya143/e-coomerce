from django.contrib import admin
from django.urls import path
from .import views
from django.conf.urls.static import static
from django.conf import settings
from .views import CheckoutView
urlpatterns=[
    path("",views.store,name='store'),
    path('<slug:category_slug>/',views.store,name='products_by_category'),
    path('<slug:category_slug>/<slug:product_slug>/',views.product_detail,name='product_detail'),
    path('products/<str:audience>/', views.products_by_audience, name='product_by_audience'),
    path('check',CheckoutView.as_view(),name='checkout'),
] 