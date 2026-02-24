from django.contrib import admin
from .models import Order, OrderProduct
from django.utils.html import format_html


class OrderProductInline(admin.TabularInline):
    model = OrderProduct
    extra = 0
    readonly_fields = ('product', 'quantity', 'product_price')
    can_delete = False

class OrderAdmin(admin.ModelAdmin):

    list_display = (
        'id',
        'user',
        'customer_name',
        'phone',
        'city',
        'formatted_total',
        'payment_method',
        'colored_status',
        'created_at',
    )

    list_display_links = ('id', 'customer_name')

    list_filter = ('status', 'payment_method', 'created_at')

    search_fields = (
        'id',
        'first_name',
        'last_name',
        'phone',
        'email',
    )

    ordering = ('-created_at',)

    list_per_page = 25

    readonly_fields = ('created_at',)

    inlines = [OrderProductInline]

    fieldsets = (
    ('👤 Customer Information', {
        'fields': ('user', 'first_name', 'last_name', 'phone', 'email')
    }),
    ('🏠 Shipping Address', {
        'fields': ('address', 'city', 'state', 'pincode')
    }),
    ('💳 Payment Details', {
        'fields': ('total_price', 'payment_method', 'status')
    }),
    ('📅 Other Info', {
        'fields': ('created_at',)
    }),
    )
    def customer_name(self, obj):
        return f"{obj.first_name} {obj.last_name}"

    def formatted_total(self, obj):
        return f"₹ {obj.total_price}"

    def colored_status(self, obj):
        if obj.status == "Completed":
            color = "green"
        elif obj.status == "Cancelled":
            color = "red"
        elif obj.status == "Accepted":
            color = "blue"
        else:
            color = "orange"

        return format_html(
            '<strong style="color: {};">{}</strong>',
            color,
            obj.status
        )
admin.site.register(Order,OrderAdmin)
admin.site.register(OrderProduct)