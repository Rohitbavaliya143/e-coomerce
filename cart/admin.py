# from django.contrib import admin
# from .models import Cart,CartItem


# class CartAdmin(admin.ModelAdmin):
#     list_display = ('id', 'user', 'cart_id', 'date_added')
#     list_filter = ('date_added',)
#     search_fields = ('user__email', 'cart_id')


# class CartItemAdmin(admin.ModelAdmin):
#     list_display = ('id', 'product', 'cart', 'quantity', 'is_active', 'created_at')
#     list_filter = ('is_active', 'created_at')
#     search_fields = ('product__product_name',)

# admin.site.register(Cart,CartAdmin)
# admin.site.register(CartItem,CartItemAdmin)

from django.contrib import admin
from .models import Cart, CartItem


@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'cart_id', 'date_added')
    list_filter = ('date_added',)
    search_fields = ('user__email', 'cart_id')
    readonly_fields = ('date_added',)
    ordering = ('-date_added',)


@admin.register(CartItem)
class CartItemAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'product',
        'cart',
        'quantity',
        'is_active',
        'created_at',
        'updated_at',
        'sub_total'
    )

    list_filter = ('is_active', 'created_at')
    search_fields = ('product__product_name',)
    readonly_fields = ('created_at', 'updated_at')
    ordering = ('-created_at',)


