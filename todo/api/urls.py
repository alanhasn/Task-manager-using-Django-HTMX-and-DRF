from django.urls import path
from drf_spectacular.views import (SpectacularAPIView, SpectacularRedocView,
                                   SpectacularSwaggerView)
from rest_framework_simplejwt.views import (TokenObtainPairView,
                                            TokenRefreshView, TokenVerifyView)

from .views import (DetailUpdateDeleteTodoAPIView, ListCreateTodosAPIView,
                    RegisterAPIView, UsersAPIView)

app_name = "api"

urlpatterns = [
    path("todos/", ListCreateTodosAPIView.as_view(), name="list-todos"),
    path("todos/<int:pk>/", DetailUpdateDeleteTodoAPIView.as_view(), name="detail-todos"),
    path("users/", UsersAPIView.as_view(), name="current-user"),

    # JWT Authentication    
    path('register/', RegisterAPIView.as_view(), name='register'),
    path('login/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('token/verify/', TokenVerifyView.as_view(), name='token_verify'),

    # API Documantation
    path('schema/', SpectacularAPIView.as_view(), name='schema'),
    # swager and redoc UI:
    path('schema/swagger-ui/', SpectacularSwaggerView.as_view(url_name='api:schema'), name='swagger-ui'),
    path('schema/redoc/', SpectacularRedocView.as_view(url_name='api:schema'), name='redoc'),



]