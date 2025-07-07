# =========== IMPORTS ===========
from django.contrib.auth import logout as auth_logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.auth.tokens import default_token_generator
from django.contrib.auth.views import LoginView
from django.contrib.sites.shortcuts import get_current_site
from django.core.exceptions import ValidationError
from django.core.mail import send_mail
from django.core.validators import validate_email
from django.shortcuts import HttpResponse, redirect, render
from django.template.loader import render_to_string
from django.urls import reverse_lazy
from django.utils.encoding import force_bytes, force_str
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.views.generic import TemplateView
from django.views.generic.edit import FormView

from decouple import config
from .forms import CustomUserCreationForm


# REGISTER USER VIEW
class RegisterView(FormView):
    template_name = "account/registration/signup.html"
    form_class = CustomUserCreationForm
    success_url = reverse_lazy("accounts:activation_sent")

    # This method is called when the form is valid
    def form_valid(self, form):
        user = form.save(commit=False)
        user.is_active=False # Deactivate the account
        user.save()

        # Send email verification
        current_site = get_current_site(self.request) # get current site
        subject = 'Activate Your Account'

        message = render_to_string('account/email_verification.html', {
            'user': user,
            'domain': current_site.domain,
            'uid': urlsafe_base64_encode(force_bytes(user.pk)),
            'token': default_token_generator.make_token(user),
        })
        send_mail(subject, message, config("EMAIL_HOST_USER") , [user.email]) 

        return super().form_valid(form)
    
    # This method is called to check if the user is authenticated
    # If they are, it redirects them to the home page
    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect("todos:home")
        return super().dispatch(request, *args, **kwargs)

# LOGIN VIEW
class CustomLoginView(LoginView):
    template_name = "account/registration/login.html"
    redirect_authenticated_user = True # Redirect authenticated users to the home page
    
    # This method is called to get the success URL after login
    def get_success_url(self):
        return reverse_lazy("todos:home")

# LOGOUT VIEW USING FUNCTION BASED VIEW
@login_required(login_url="accounts:login")
def logout_view(request):
    auth_logout(request)  # Remove the user from the session
    return redirect("accounts:login")

def activate(request, uidb64, token):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except Exception:
        user = None

    if user and default_token_generator.check_token(user, token):
        user.is_active = True
        user.save()
        return render(request,"account/account_activated.html")
    else:
        return HttpResponse("Activation link is invalid!,Try Again")

class ActivationSentView(TemplateView):
    template_name = "account/activation_sent.html"


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


# 404 page not found view
# def not_found_view(request , exception=True):
#     return render(request , "account/404.html" , status=403)