# =========== IMPORTS ===========
from django.contrib import messages
from django.shortcuts import HttpResponse , render
from django.contrib.auth import login as auth_login
from django.contrib.auth import logout as auth_logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView
from django.shortcuts import redirect
from django.core.validators import validate_email
from django.core.exceptions import ValidationError
from django.urls import reverse_lazy
from django.views.generic.edit import FormView
from django.contrib.auth.models import User
from django.contrib.auth import get_user_model
from .forms import CustomUserCreationForm

# def register(request):
#     form = CustomUserCreationForm(request.POST)
#     if request.user.is_authenticated:
#         return redirect("todos:home")
    
#     if request.headers.get("HX-Request") == "true":
#         username = form.cleaned_data.get("username")
#         if User.objects.filter(username=username).exists():
#             return HttpResponse("This username is already exist")
#         else: 
#             return HttpResponse("this username is Available")
        
#     if request.method == "POST":
#         if form.is_valid():
#             user = form.save()
#             auth_login(request , user)
#             return redirect("todos:home")
#         return render(request ,"registration/signup.html" , {"form":form} )
        
    # return render(request , "registration/signup.html" , {"form":form})

# REGISTER USER VIEW
class RegisterView(FormView):
    template_name = "registration/signup.html"
    form_class = CustomUserCreationForm
    success_url = reverse_lazy("todos:home")

    # This method is called when the form is valid
    # It saves the user and logs them in
    def form_valid(self, form):
        user = form.save()
        auth_login(self.request , user=user )
        return super().form_valid(form)
    
    # This method is called to check if the user is authenticated
    # If they are, it redirects them to the home page
    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect("todos:home")
        return super().dispatch(request, *args, **kwargs)

# LOGIN VIEW
class CustomLoginView(LoginView):
    template_name = "registration/login.html"
    redirect_authenticated_user = True # Redirect authenticated users to the home page
    
    # This method is called to get the success URL after login
    def get_success_url(self):
        return reverse_lazy("todos:home")

# LOGOUT VIEW USING FUNCTION BASED VIEW
@login_required(login_url="accounts:login")
def logout_view(request):
    auth_logout(request)  # Remove the user from the session
    return redirect("accounts:login")




# ======= HTMX View for Checking username and email =======
def check_username(request):
    username = request.POST.get("username", "")

    if username == "":
        return HttpResponse('<p class="text-error text-sm mt-1">This field cannot be empty</p>')
    
    if User.objects.filter(username=username).exists():
        return HttpResponse('<p class="text-error text-sm mt-1">This username already exists</p>')
    
    return HttpResponse('<p class="text-success text-sm mt-1">This username is available ✓</p>')
    
def check_email(request):
    email = request.POST.get('email', '').strip()

    if not email:
        return HttpResponse('<p class="text-error">Email field cannot be empty.</p>')

    try:
        validate_email(email) # validate email from Django
    except ValidationError:
        return HttpResponse('<p class="text-error">Invalid email format.</p>')

    if User.objects.filter(email=email).exists():
        return HttpResponse('<p class="text-error">This email already registered.</p>')

    return HttpResponse('<p class="text-success">Email is available ✓</p>')
