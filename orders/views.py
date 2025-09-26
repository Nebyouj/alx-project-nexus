import os, uuid, requests
from decimal import Decimal
from django.db import transaction
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse
from rest_framework import viewsets, status, permissions, generics
from rest_framework.decorators import action, api_view, permission_classes
from rest_framework.response import Response
from .models import Order, OrderItem
from .serializers import OrderSerializer, OrderItemSerializer
from products.models import Product
from accounts.tasks import send_email

CHAPA_SECRET_KEY = os.getenv("CHAPA_SECRET_KEY")
CHAPA_BASE_URL = "https://api.chapa.co/v1"

class CheckoutViewSet(viewsets.GenericViewSet):
    """
    Creates an Order, validates stock, and returns a Chapa checkout URL.
    """
    permission_classes = [permissions.AllowAny]
    # permission_classes = [permissions.IsAuthenticated]
    serializer_class = OrderSerializer

    @action(detail=False, methods=["post"], url_path="checkout")
    def checkout(self, request):
        """
        POST payload:
        {
          "items": [
            {"product_slug": "headphones", "quantity": 2},
            {"product_slug": "book-1", "quantity": 1}
          ],
          "currency": "ETB",
          "metadata": {"notes": "deliver to ..."}   # optional
        }
        """
        data = request.data
        items = data.get("items", [])
        currency = data.get("currency", "ETB")
        metadata = data.get("metadata", {})

        if not items:
            return Response({"detail": "No items provided."},
                            status=status.HTTP_400_BAD_REQUEST)

        user = request.user

        with transaction.atomic():
            order = Order.objects.create(
                user=user,
                currency=currency,
                metadata=metadata
            )

            total = Decimal("0.00")
            order_items = []

            for it in items:
                product_slug = it.get("product_slug")
                qty = int(it.get("quantity", 1))

                try:
                    product = Product.objects.select_for_update().get(
                        slug=product_slug, is_active=True
                    )
                except Product.DoesNotExist:
                    transaction.set_rollback(True)
                    return Response(
                        {"detail": f"Product {product_slug} not found or inactive."},
                        status=status.HTTP_400_BAD_REQUEST
                    )

                if product.stock < qty:
                    transaction.set_rollback(True)
                    return Response(
                        {"detail": f"Insufficient stock for {product.title}."},
                        status=status.HTTP_400_BAD_REQUEST
                    )

                unit_price = product.price
                line_total = unit_price * qty
                total += line_total

                order_items.append(
                    OrderItem(
                        order=order,
                        product=product,
                        unit_price=unit_price,
                        quantity=qty,
                        line_total=line_total
                    )
                )

            OrderItem.objects.bulk_create(order_items)
            order.total_amount = total
            order.save()

            # --- Chapa payment initialization ---
            tx_ref = str(uuid.uuid4())
            callback_url = request.build_absolute_uri("/api/payments/webhook/")

            payload = {
                "amount": str(total),          # Chapa expects string
                "currency": currency,
                "email": user.email,
                "first_name": user.first_name or "User",
                "last_name": user.last_name or "",
                "tx_ref": tx_ref,
                "callback_url": callback_url,
                "return_url": "https://your-frontend.com/payment-success",
            }
            headers = {"Authorization": f"Bearer {CHAPA_SECRET_KEY}"}

            try:
                resp = requests.post(
                    f"{CHAPA_BASE_URL}/transaction/initialize",
                    json=payload,
                    headers=headers,
                    timeout=15,
                )
                resp.raise_for_status()
            except requests.RequestException as e:
                transaction.set_rollback(True)
                return Response(
                    {"detail": "Error contacting Chapa", "error": str(e)},
                    status=status.HTTP_502_BAD_GATEWAY,
                )

            chapa_data = resp.json()
            checkout_url = chapa_data.get("data", {}).get("checkout_url")
            if not checkout_url:
                transaction.set_rollback(True)
                return Response(
                    {"detail": "Failed to obtain Chapa checkout URL."},
                    status=status.HTTP_502_BAD_GATEWAY,
                )

            # Save reference for later verification
            order.payment_reference = tx_ref
            order.save()
            # After order is created
            send_email(
                subject=f"Order #{Order.id} Created",
                message=f"Hi {Order.user.username}, your order has been created. Total: {order.total_amount} {order.currency}",
                recipient=[Order.user.email]
            )

        return Response(
            {
                "order_id": order.id,
                "checkout_url": checkout_url,
                "amount": str(order.total_amount),
                "currency": order.currency,
                "status": order.status,
            },
            status=status.HTTP_201_CREATED,
        )


class UserOrderListView(generics.ListAPIView):
    serializer_class = OrderSerializer
    permission_classes = [permissions.IsAuthenticated]
    # permission_classes = [permissions.AllowAny]

    def get_queryset(self):
        return Order.objects.filter(
            user=self.request.user
        ).prefetch_related("items__product")


class UserOrderDetailView(generics.RetrieveAPIView):
    serializer_class = OrderSerializer
    permission_classes = [permissions.IsAuthenticated]
    # permission_classes = [permissions.AllowAny]
    lookup_field = "pk"

    def get_queryset(self):
        return Order.objects.filter(
            user=self.request.user
        ).prefetch_related("items__product")


# ------------------ Chapa Webhook ------------------
@api_view(["POST"])
@permission_classes([permissions.AllowAny])   # Chapa won't send JWT
@csrf_exempt
def chapa_webhook(request):
    """
    Handle Chapa's payment status notification.
    """
    data = request.data
    tx_ref = data.get("tx_ref")
    status_ = data.get("status")

    if not tx_ref:
        return Response({"message": "tx_ref is required."}, status=400)

    try:
        order = Order.objects.get(payment_reference=tx_ref)
    except Order.DoesNotExist:
        return Response({"message": "Order not found."}, status=404)

    if status_ == "success":
        with transaction.atomic():
            if order.status != Order.Status.PAID:
                order.status = Order.Status.PAID
                order.save()
                for item in order.items.select_related("product"):
                    product = item.product
                    product.stock -= item.quantity
                    product.save()
                # After payment success
                send_email(
                    subject=f"Order #{order.id} Paid",
                    message=f"Hi {order.user.username}, your payment was successful. Thank you!",
                    recipient=[order.user.email]
                )
        return Response({"message": f"Order {order.id} marked as PAID."}, status=200)
    elif status_ == "failed":
        order.status = Order.Status.FAILED
        order.save()
        # After payment failure
        send_email(
            subject=f"Order #{order.id} Payment Failed",
            message=f"Hi {order.user.username}, your payment failed. Please try again.",
            recipient=[order.user.email]
        )
        return Response({"message": f"Order {order.id} marked as FAILED."}, status=200)
    else:
        return Response({"message": f"Unknown status '{status_}'."}, status=400)





