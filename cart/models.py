# from django.db import models
# from store.models import Product
# from django.conf import settings
# from accounts.models import Account

# class Cart(models.Model):
#     user = models.ForeignKey(Account, on_delete=models.CASCADE, null=True, blank=True)
#     date_added = models.DateField(auto_now_add=True)
#     def __str__(self):
#         return self.user
    

# class CartItem(models.Model):
#     product = models.ForeignKey(Product,on_delete=models.CASCADE)
#     cart = models.ForeignKey(Cart,on_delete=models.CASCADE)
#     quantity = models.IntegerField()
#     is_active=models.BooleanField(default=True)

#     def sub_total(self):
#         return self.product.price * self.quantity
#     def __str__(self):
#         return f"{self.product.product_name} ({ self.quantity })"



from django.db import models
from django.conf import settings
from store.models import Product
from accounts.models import Account
import uuid


# class Cart(models.Model):
#     user = models.ForeignKey(
#         Account,
#         on_delete=models.CASCADE,
#         null=True,
#         blank=True,
#         related_name='carts'          # user.carts.all() થી બધા carts મળે
#     )
#     cart_id = models.CharField(
#         max_length=36,                # uuid4 ના માટે 36 chars
#         unique=True,
#         blank=True,
#         null=True,
#         help_text="Session-based identifier for guest carts"
#     )
#     date_added = models.DateField(auto_now_add=True)
#     updated_at = models.DateTimeField(auto_now=True)   # last modified track કરવા

#     class Meta:
#         verbose_name = 'Cart'
#         verbose_name_plural = 'Carts'
#         ordering = ['-date_added']
#         indexes = [
#             models.Index(fields=['cart_id']),
#             models.Index(fields=['user']),
#         ]

#     def __str__(self):
#         if self.user:
#             return f"Cart for {self.user.email or self.user.username} ({self.id})"
#         if self.cart_id:
#             return f"Guest Cart {self.cart_id[:8]}..."
#         return f"Cart #{self.id} (anonymous)"

#     def total_items(self):
#         return self.cartitem_set.count()   # અથવા .aggregate થી sum

#     def total_price(self):
#         return sum(item.sub_total() for item in self.cartitem_set.all())


# class CartItem(models.Model):
#     cart = models.ForeignKey(
#         Cart,
#         on_delete=models.CASCADE,
#         related_name='items'           # ← આથી cart.items.all() થશે
#     )
#     product = models.ForeignKey(
#         Product,
#         on_delete=models.CASCADE,
#         related_name='cart_items'
#     )
#     quantity = models.PositiveIntegerField(
#         default=1,
#         help_text="Number of items (must be positive)"
#     )
#     is_active = models.BooleanField(default=True)
#     added_at = models.DateTimeField(auto_now_add=True)

#     class Meta:
#         verbose_name = 'Cart Item'
#         verbose_name_plural = 'Cart Items'
#         unique_together = [['cart', 'product']]   # એક cart માં એક product એક જ વખત
#         ordering = ['-added_at']

#     def sub_total(self):
#         return self.product.price * self.quantity

#     def __str__(self):
#         return f"{self.product.product_name} × {self.quantity} (in cart {self.cart_id_short})"

#     @property
#     def cart_id_short(self):
#         return str(self.cart.cart_id)[:8] if self.cart.cart_id else f"#{self.cart.id}"





class Cart(models.Model):
    user       = models.ForeignKey(Account, on_delete=models.CASCADE, null=True, blank=True)
    cart_id    = models.CharField(max_length=50, blank=True, null=True, unique=True)
    date_added = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.cart_id or f"User cart {self.user}"

class CartItem(models.Model):
    product  = models.ForeignKey(Product, on_delete=models.CASCADE)
    cart     = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name='items')
    quantity = models.PositiveIntegerField(default=1)
    is_active = models.BooleanField(default=True)


    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def sub_total(self):
        return self.product.price * self.quantity
    
