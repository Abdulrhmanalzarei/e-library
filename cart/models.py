from django.db import models
from django.conf import settings
from books.models import Book

class CartItem(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="cart_items")
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    added_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("user", "book")

    def subtotal(self):
        return self.book.price * self.quantity

    def __str__(self):
        return f"{self.quantity} x {self.book.title}"
