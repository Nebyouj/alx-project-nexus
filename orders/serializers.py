# orders/serializers.py
from rest_framework import serializers
from .models import Order, OrderItem
from products.serializers import ProductSerializer
from products.models import Product
from django.db import transaction
from decimal import Decimal

class OrderItemSerializer(serializers.ModelSerializer):
    product = ProductSerializer(read_only=True)
    product_slug = serializers.SlugField(write_only=True, required=True)
    class Meta:
        model = OrderItem
        fields = ["id", "product", "product_slug", "unit_price", "quantity", "line_total"]
        read_only_fields = ["id", "product", "unit_price", "line_total"]

class OrderSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many=True)
    status = serializers.CharField(read_only=True)
    stripe_payment_intent = serializers.CharField(read_only=True)

    class Meta:
        model = Order
        fields = ["id", "user", "items", "total_amount", "currency", "status", "stripe_payment_intent", "created_at"]
        read_only_fields = ["id", "user", "total_amount", "currency", "status", "stripe_payment_intent", "created_at"]

    def create(self, validated_data):
        # Order creation occurs in view (we want to return payment info there)
        raise NotImplementedError("Order creation handled in Checkout view.")
