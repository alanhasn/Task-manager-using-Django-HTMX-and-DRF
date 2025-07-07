from django.urls import path

from .views import *

app_name = "accounts"

urlpatterns = [
    # URL patterns for user authentication
    path('signup/', RegisterView.as_view(), name='signup'),
    path('login/', CustomLoginView.as_view() , name='login'),
    path('logout/',logout_view, name='logout'),
    path("activation-sent/", ActivationSentView.as_view(), name="activation_sent"),
    path('activate/<uidb64>/<token>/', activate, name='activate'),

]

hx_urlpatterns=[
    path("check_username/" , check_username , name="check_username"),
    path("check_email/" , check_email , name="check_email")
]

urlpatterns += hx_urlpatterns