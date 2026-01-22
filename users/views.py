from django.shortcuts import render, redirect
from django.contrib.auth import login,logout
from django.contrib import messages
from .forms import RegisterForm
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth.decorators import login_required

@login_required
def user_logout(request):
    logout(request)
    return redirect("users:login")

class CustomLoginView(LoginView):
    template_name = "users/login.html"

class CustomLogoutView(LogoutView):
    next_page = "/"

def register_view(request):
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, "Account created successfully.")
            return redirect("books:book_list")
    else:
        form = RegisterForm()
    return render(request, "users/register.html", {"form": form})
