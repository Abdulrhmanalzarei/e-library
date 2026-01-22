# books/forms.py
from django import forms
from .models import Book, Author, Category

class BookForm(forms.ModelForm):
    class Meta:
        model = Book
        fields = ["title", "authors", "categories", "description", "price", "stock", "isbn", "cover"]
        widgets = {
            "authors": forms.SelectMultiple(attrs={"class": "form-select", "size": 6}),
            "categories": forms.SelectMultiple(attrs={"class": "form-select", "size": 6}),
            "description": forms.Textarea(attrs={"rows": 4, "class": "form-control"}),
            "title": forms.TextInput(attrs={"class": "form-control"}),
            "price": forms.NumberInput(attrs={"class": "form-control", "step": "0.01"}),
            "stock": forms.NumberInput(attrs={"class": "form-control"}),
            "isbn": forms.TextInput(attrs={"class": "form-control"}),
            "cover": forms.ClearableFileInput(attrs={"class": "form-control"}),
        }

class AuthorForm(forms.ModelForm):
    class Meta:
        model = Author
        fields = ["name", "bio"]
        widgets = {
            "name": forms.TextInput(attrs={"class": "form-control"}),
            "bio": forms.Textarea(attrs={"class": "form-control", "rows": 3}),
        }

class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ["name"]
        widgets = {
            "name": forms.TextInput(attrs={"class": "form-control"}),
        }
