# =========== IMPORTS ===========
from django.contrib import messages
from django.contrib.auth import login as auth_login
from django.contrib.auth import logout as auth_logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic.edit import FormView

from .forms import CustomUserCreationForm

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
