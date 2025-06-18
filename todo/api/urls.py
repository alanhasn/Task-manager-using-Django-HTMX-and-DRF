from django.urls import path
from .views import (
                    ListCreateTodosAPIView, 
                    UsersAPIView,
                    DetailUpdateDeleteTodoAPIView,
                    RegisterAPIView
                )
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenVerifyView
)
from drf_spectacular.views import (
    SpectacularAPIView,
    SpectacularRedocView, 
    SpectacularSwaggerView
)

urlpatterns = [
    path("todos/", ListCreateTodosAPIView.as_view(), name="list-todos"),
    path("todos/<int:pk>/", DetailUpdateDeleteTodoAPIView.as_view(), name="detail-todos"),
    path("users/", UsersAPIView.as_view(), name="current-user"),
    path('register/', RegisterAPIView.as_view(), name='register'),

    # JWT Authentication    
    path('login/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('token/verify/', TokenVerifyView.as_view(), name='token_verify'),

    # API Documantation
    path('schema/', SpectacularAPIView.as_view(), name='schema'),
    # swager and redoc UI:
    path('schema/swagger-ui/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
    path('schema/redoc/', SpectacularRedocView.as_view(url_name='schema'), name='redoc'),



]