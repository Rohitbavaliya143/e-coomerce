from django.conf import settings
from django.db import models
import uuid


class Order(models.Model):
    STATUS = (
         ('New', 'New'),
         ('Accepted', 'Accepted'),
         ('Shipped', 'Shipped'),
         ('Completed', 'Completed'),
         ('Cancelled', 'Cancelled'),
    )

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE
    )

    order_number = models.CharField(max_length=20, blank=True)

    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    phone = models.CharField(max_length=15)
    email = models.EmailField(max_length=50)
    address = models.CharField(max_length=200)
    city = models.CharField(max_length=50)
    state = models.CharField(max_length=50)
    pincode = models.CharField(max_length=10)
    tax = models.FloatField(default=0.0)
    total_price = models.FloatField(default=0.0)
    payment_method = models.CharField(max_length=50, default='COD')
    
    status = models.CharField(max_length=20, choices=STATUS, default='New')
    created_at = models.DateTimeField(auto_now_add=True)
    
    def save(self, *args, **kwargs):

        # order_number generate
        if not self.order_number:
            self.order_number = "ORD" + str(uuid.uuid4().hex[:8]).upper()

        # -------- STOCK RETURN LOGIC ----------
        if self.pk:
            old_order = Order.objects.get(pk=self.pk)

            # Cancel detect
            if old_order.status != 'Cancelled' and self.status == 'Cancelled':

                order_products = self.orderproduct_set.all()

                for item in order_products:
                    product = item.product
                    product.stock += item.quantity
                    product.save()

        super().save(*args, **kwargs)

    def __str__(self):
        return self.order_number

class OrderProduct(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    # Assuming you have a Product model in an app named 'store'
    product = models.ForeignKey('store.Product', on_delete=models.CASCADE) 
    quantity = models.IntegerField()
    product_price = models.FloatField()
    ordered = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.product.product_name} x {self.quantity}"