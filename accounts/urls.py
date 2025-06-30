from django.urls import path

from .views import *

app_name = "accounts"

urlpatterns = [
    # URL patterns for user authentication
    path('signup/', RegisterView.as_view(), name='signup'),
    path('login/', CustomLoginView.as_view() , name='login'),
    path('logout/',logout_view, name='logout'),
]