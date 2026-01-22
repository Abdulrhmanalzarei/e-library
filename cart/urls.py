from django.urls import path
from .views import add_to_cart, view_cart, update_cart, remove_item

app_name = "cart"

urlpatterns = [
    path("add/", add_to_cart, name="add_to_cart"),
    path("", view_cart, name="view_cart"),
    path("update/", update_cart, name="update_cart"),
    path("remove/<int:pk>/", remove_item, name="remove_item"),
]
