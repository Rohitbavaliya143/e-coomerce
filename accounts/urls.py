from django.urls import path
from .import views
from django.contrib.auth.views import LogoutView

urlpatterns=[
    path('register',views.register,name='register'),
    path('login/',views.login_view,name='login'),
    path('logout/',LogoutView.as_view(next_page='home'), name='logout'),
    path('contact/',views.contact,name='contact'),
    path('dashboard/',views.dashboard,name='dashboard'),
    path('edit-profile/',views.edit_profile,name='edit_profile'),
    path('change-password/',views.change_password,name='change_password'),
    path('my-orders/',views.my_orders,name='my_orders'),
    # path('order/<str:order_number>/', views.order_detail, name='order_detail'),
    path('cancel-order/<str:order_number>/', views.cancel_order, name='cancel_order'),
    path('<slug:category_slug>/<slug:product_slug>/',views.product_detail, name='product_detail'),
]