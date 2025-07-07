from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path('admin/', admin.site.urls),
    path("api/", include("todo.api.urls" , namespace="api")),
    path("", include('todo.urls' , namespace="todo")),
    path('accounts/', include("accounts.urls" , namespace="accounts")),

    # Social auth (will be on /social-auth/)
    path('social-auth/', include('social_django.urls', namespace='social')),

]

# Custom 404 URL handler
# handler404 = "accounts.views.not_found_view"
