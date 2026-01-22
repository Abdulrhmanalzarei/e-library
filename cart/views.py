from django.shortcuts import redirect, render, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import CartItem
from books.models import Book
from django.contrib import messages

@login_required
def add_to_cart(request):
    if request.method == "POST":
        book_id = request.POST.get("book_id")
        qty = int(request.POST.get("quantity", 1))
        book = get_object_or_404(Book, id=book_id)
        if qty < 1:
            messages.error(request, "Quantity must be at least 1.")
            return redirect("books:book_detail", slug=book.slug)
        if qty > book.stock:
            messages.error(request, "Not enough stock available.")
            return redirect("books:book_detail", slug=book.slug)
        item, created = CartItem.objects.get_or_create(user=request.user, book=book, defaults={"quantity": qty})
        if not created:
            item.quantity += qty
            if item.quantity > book.stock:
                item.quantity = book.stock
            item.save()
        messages.success(request, f"Added {qty} x {book.title} to your cart.")
        return redirect("cart:view_cart")
    return redirect("books:book_list")

@login_required
def view_cart(request):
    items = CartItem.objects.filter(user=request.user).select_related("book")
    total = sum([it.subtotal() for it in items])
    return render(request, "cart/cart.html", {"items": items, "total": total})

@login_required
def update_cart(request):
    if request.method == "POST":
        for key, val in request.POST.items():
            if key.startswith("qty_"):
                try:
                    pk = int(key.split("_", 1)[1])
                    qty = int(val)
                    item = CartItem.objects.get(pk=pk, user=request.user)
                    if qty <= 0:
                        item.delete()
                    else:
                        if qty > item.book.stock:
                            qty = item.book.stock
                        item.quantity = qty
                        item.save()
                except Exception:
                    pass
        messages.success(request, "Cart updated.")
    return redirect("cart:view_cart")

@login_required
def remove_item(request, pk):
    item = get_object_or_404(CartItem, pk=pk, user=request.user)
    item.delete()
    messages.success(request, "Item removed.")
    return redirect("cart:view_cart")
