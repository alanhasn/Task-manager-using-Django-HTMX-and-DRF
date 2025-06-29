from django.shortcuts import render, redirect
from .forms import CustomUserCreationForm
from django.contrib.auth import login as auth_login, authenticate, logout as auth_logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages

# Signup view for user registration
def signup(request):
    if request.user.is_authenticated:
        return redirect("todos:home")
    
    if request.method == "POST":
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            auth_login(request, user) # Automatically log in the user after registration
            return redirect("todos:home")
    else:
        form = CustomUserCreationForm()
    return render(request, "registration/signup.html", {"form": form})

# Login view for user authentication
def login_view(request):
    if request.user.is_authenticated:
        return redirect("todos:home")
    
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        user = authenticate(request, username=username, password=password)

        if user is not None:
            auth_login(request, user)
            return redirect("todos:home")
        else:
            return render(request, "registration/login.html", {"error": "Invalid credentials"})

    return render(request, "registration/login.html")

@login_required(login_url="accounts:login")
def logout_view(request):
    auth_logout(request)
    messages.success(request, "You have been logged out successfully.")
    return redirect("accounts:login")
