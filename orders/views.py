from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from cart.models import CartItem
from .models import Order, OrderItem
from django.contrib import messages
from django.db import transaction

@login_required
def checkout(request):
    items = CartItem.objects.filter(user=request.user).select_related("book")
    if not items.exists():
        messages.error(request, "Your cart is empty.")
        return redirect("books:book_list")
    with transaction.atomic():
        total = 0
        for it in items:
            if it.quantity > it.book.stock:
                messages.error(request, f"Insufficient stock: {it.book.title}")
                return redirect("cart:view_cart")
            total += it.subtotal()
        order = Order.objects.create(user=request.user, total=total, status="paid")
        for it in items:
            OrderItem.objects.create(order=order, book=it.book, quantity=it.quantity, price=it.book.price)
            it.book.stock -= it.quantity
            it.book.save()
        items.delete()
    messages.success(request, f"Order #{order.pk} created successfully.")
    return redirect("orders:order_confirmation", pk=order.pk)

@login_required
def order_confirmation(request, pk):
    order = get_object_or_404(Order, pk=pk, user=request.user)
    return render(request, "orders/order_confirmation.html", {"order": order})

@login_required
def my_orders(request):
    qs = Order.objects.filter(user=request.user).order_by("-created_at")
    return render(request, "orders/my_orders.html", {"orders": qs})
