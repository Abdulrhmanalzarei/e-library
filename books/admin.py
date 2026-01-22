from django.contrib import admin
from .models import Book, Author, Category

@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ("title", "price", "stock", "created_at")
    prepopulated_fields = {"slug": ("title",)}
    search_fields = ("title", "authors__name", "isbn")
    list_filter = ("categories",)

admin.site.register(Author)
admin.site.register(Category)
