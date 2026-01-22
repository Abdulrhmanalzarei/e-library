from django.urls import path
from . import views

app_name = "books"

urlpatterns = [
   
    path("", views.book_list, name="book_list"),
    path("add/", views.book_create, name="book_create"),
    path("delete/<int:pk>/", views.book_delete, name="book_delete"),

    
    path("authors/", views.authors_list, name="authors_list"),
    path("authors/add/", views.author_create, name="author_create"),
    path("authors/delete/<int:pk>/", views.author_delete, name="author_delete"),

    
    path("categories/", views.categories_list, name="categories_list"),
    path("categories/add/", views.category_create, name="category_create"),
    path("categories/delete/<int:pk>/", views.category_delete, name="category_delete"),

    
    path("<slug:slug>/", views.book_detail, name="book_detail"),
]
