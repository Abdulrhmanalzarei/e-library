from django.urls import path
from .views import checkout, order_confirmation, my_orders

app_name = "orders"

urlpatterns = [
    path("checkout/", checkout, name="checkout"),
    path("confirmation/<int:pk>/", order_confirmation, name="order_confirmation"),
    path("my/", my_orders, name="my_orders"),
]
