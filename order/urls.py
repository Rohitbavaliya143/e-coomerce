from django.urls import path
from store.views import CheckoutView
from .views import order_complete,order_detail


urlpatterns=[
    path('order_complete/<str:order_number>/',order_complete,name='order_complete'),
    path('order/<str:order_number>/',order_detail,name='order_detail'),
]