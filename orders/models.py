# orders/models.py
from django.db import models
from django.conf import settings
from django.utils.translation import gettext_lazy as _
from products.models import Product
from decimal import Decimal

User = settings.AUTH_USER_MODEL

class Order(models.Model):
    class Status(models.TextChoices):
        PENDING = "PENDING", _("Pending")
        PAID = "PAID", _("Paid")
        CANCELED = "CANCELED", _("Canceled")
        FAILED = "FAILED", _("Failed")

    user = models.ForeignKey(User, related_name="orders", on_delete=models.CASCADE)
    total_amount = models.DecimalField(max_digits=12, decimal_places=2, default=Decimal("0.00"))
    currency = models.CharField(max_length=10, default="usd")
    payment_reference = models.CharField(max_length=255, blank=True, null=True)
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.PENDING)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    metadata = models.JSONField(blank=True, null=True)  # optional, store extra info

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"Order #{self.id} - {self.user} - {self.status}"

class OrderItem(models.Model):
    order = models.ForeignKey(Order, related_name="items", on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.PROTECT)
    unit_price = models.DecimalField(max_digits=12, decimal_places=2)  # snapshot of price
    quantity = models.PositiveIntegerField()
    line_total = models.DecimalField(max_digits=12, decimal_places=2)

    def save(self, *args, **kwargs):
        self.line_total = (self.unit_price * self.quantity)
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.quantity}x {self.product.title} (Order {self.order.id})"
