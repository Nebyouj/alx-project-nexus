from django.urls import path
from rest_framework.routers import DefaultRouter
from .views import (
    CheckoutViewSet,
    UserOrderListView,
    UserOrderDetailView,
    chapa_webhook,
)

router = DefaultRouter()
checkout = CheckoutViewSet.as_view({"post": "checkout"})

urlpatterns = [
    path("orders/checkout/", checkout, name="orders-checkout"),
    path("orders/", UserOrderListView.as_view(), name="user-orders"),
    path("orders/<int:pk>/", UserOrderDetailView.as_view(), name="user-order-detail"),
    path("payments/webhook/", chapa_webhook, name="chapa-webhook"),
]
