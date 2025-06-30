from django.urls import path

from .views import *

app_name = "accounts"

urlpatterns = [
    # URL patterns for user authentication
    path('signup/', signup, name='signup'),
    path('login/', login_view , name='login'),
    path('logout/', logout_view, name='logout'),
]