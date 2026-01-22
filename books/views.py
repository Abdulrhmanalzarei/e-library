
from django.shortcuts import render, get_object_or_404, redirect
from django.core.paginator import Paginator
from django.contrib import messages
from django.urls import reverse
from django.contrib.auth.decorators import user_passes_test, login_required
from django.db.models.deletion import ProtectedError
from .models import Book, Author, Category
from .forms import BookForm, AuthorForm, CategoryForm
from django.contrib.auth.decorators import login_required, user_passes_test

def admin_required(view_func):
    return login_required(
        user_passes_test(
            lambda u: u.is_staff,
            login_url="users:login"
        )(view_func)
    )

def book_list(request):
    books = Book.objects.filter(is_active=True)
    return render(request, "books/book_list.html", {"books": books})


def book_detail(request, slug):
    book = get_object_or_404(Book, slug=slug)
    return render(request, "books/book_detail.html", {"book": book})

# helper to restrict to staff
def staff_required(view_func):
    return user_passes_test(lambda u: u.is_staff, login_url="users:login")(view_func)

# ---------- Book create & delete ----------
@admin_required
def book_create(request):
    if request.method == "POST":
        form = BookForm(request.POST, request.FILES)
        if form.is_valid():
            book = form.save()
            messages.success(request, f"Book '{book.title}' created.")
            return redirect("books:book_list")
    else:
        form = BookForm()
    return render(request, "books/book_create.html", {"form": form})

@admin_required
def book_delete(request, pk):
    book = get_object_or_404(Book, pk=pk)
    if request.method == "POST":
        try:
            
            book.is_active = False
            book.save()
            messages.success(request, f"Book '{book.title}' has been disabled.")
        except ProtectedError:
            messages.error(request,
                f"Cannot delete '{book.title}' because it is part of previous orders."
            )
        return redirect("books:book_list")
    return render(request, "books/book_confirm_delete.html", {"object": book})


@admin_required
def author_create(request):
    if request.method == "POST":
        form = AuthorForm(request.POST)
        if form.is_valid():
            author = form.save()
            messages.success(request, f"Author '{author.name}' created.")
            return redirect("books:authors_list")
    else:
        form = AuthorForm()
    return render(request, "books/author_create.html", {"form": form})

@admin_required
def author_delete(request, pk):
    author = get_object_or_404(Author, pk=pk)
    if request.method == "POST":
        name = author.name
        author.delete()
        messages.success(request, f"Author '{name}' deleted.")
        return redirect("books:authors_list")
    return render(request, "books/author_confirm_delete.html", {"object": author})


@admin_required
def category_create(request):
    if request.method == "POST":
        form = CategoryForm(request.POST)
        if form.is_valid():
            category = form.save()
            messages.success(request, f"Category '{category.name}' created.")
            return redirect("books:categories_list")
    else:
        form = CategoryForm()
    return render(request, "books/category_create.html", {"form": form})

@admin_required
def category_delete(request, pk):
    category = get_object_or_404(Category, pk=pk)
    if request.method == "POST":
        name = category.name
        category.delete()
        messages.success(request, f"Category '{name}' deleted.")
        return redirect("books:categories_list")
    return render(request, "books/category_confirm_delete.html", {"object": category})

@staff_required
def authors_list(request):
    authors = Author.objects.all().order_by("name")
    return render(request, "books/authors_list.html", {"authors": authors})

@staff_required
def categories_list(request):
    categories = Category.objects.all().order_by("name")
    return render(request, "books/categories_list.html", {"categories": categories})