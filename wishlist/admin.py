from django.contrib import admin
from .models import Wishlist


class WishlistAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'user',
        'product',
        'created_at'
    )

    list_display_links = ('id', 'product')

    search_fields = (
        'user__email',
        'product__product_name'
    )

    list_filter = ('created_at',)


admin.site.register(Wishlist, WishlistAdmin)