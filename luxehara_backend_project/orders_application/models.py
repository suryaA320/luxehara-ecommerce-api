import uuid
from django.db import models
from django.conf import settings

class Order(models.Model):
    PAYMENT_CHOICES = (
        ("COD", "Cash On Delivery"),
        ("PREPAID", "Prepaid"),
    )

    ORDER_STATUS = (
        ("PLACED", "Placed"),
        ("PAID", "Paid"),
        ("SHIPPED", "Shipped"),
        ("DELIVERED", "Delivered"),
        ("CANCELLED", "Cancelled"),
        ("RTO", "Return To Origin"),
    )

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    customer_name = models.CharField(max_length=100)
    customer_email = models.EmailField()
    customer_mobile = models.CharField(max_length=15)

    address_line = models.TextField()
    city = models.CharField(max_length=50)
    state = models.CharField(max_length=50)
    pincode = models.CharField(max_length=10)

    payment_method = models.CharField(max_length=10, choices=PAYMENT_CHOICES)
    payment_status = models.BooleanField(default=False)

    order_status = models.CharField(
        max_length=15,
        choices=ORDER_STATUS,
        default="PLACED"
    )

    total_amount = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)

    def can_cancel(self):
        return self.order_status in ["PLACED", "PAID"]



class OrderItem(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    order = models.ForeignKey(
        "orders_application.Order",
        on_delete=models.CASCADE,
        related_name="items"
    )

    product_inventory = models.ForeignKey(
        "ecommerce_services.product_inventory",  # 👈 FIXED
        on_delete=models.PROTECT
    )

    quantity = models.PositiveIntegerField()
    price_per_unit = models.DecimalField(max_digits=10, decimal_places=2)

#  Cart 

class Cart(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    session_key = models.CharField(
        max_length=40,
        db_index=True,
        null=True,
        blank=True,
        unique=True
    )

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        null=True,
        blank=True,
        on_delete=models.CASCADE
    )

    created_at = models.DateTimeField(auto_now_add=True)



class CartItem(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    cart = models.ForeignKey(
        Cart,
        on_delete=models.CASCADE,
        related_name="items"
    )

    product_inventory = models.ForeignKey(
        "ecommerce_services.product_inventory",
        on_delete=models.CASCADE
    )

    quantity = models.PositiveIntegerField(default=1)

    class Meta:
        unique_together = ("cart", "product_inventory")

    def line_total(self):
        return self.quantity * self.product_inventory.selling_price 