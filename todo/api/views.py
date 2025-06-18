from django.contrib.auth.models import User
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, generics, permissions
from rest_framework.status import HTTP_201_CREATED, HTTP_400_BAD_REQUEST
from rest_framework.views import Response
from rest_framework_simplejwt.tokens import RefreshToken

from todo.models import Todo

from .filter import TodoFilter
from .serializer import RegisterSerializer, TodoSerializer, UserSerializer


class ListCreateTodosAPIView(generics.ListCreateAPIView):
    serializer_class = TodoSerializer
    permission_classes = [permissions.IsAuthenticated]    

    # Filterset Backend
    filter_backends = [
        DjangoFilterBackend,
        filters.SearchFilter,  
        filters.OrderingFilter,  
    ]
    filterset_class = TodoFilter
    search_fields = ['title', 'description']      
    ordering_fields = ['created_at', 'updated_at']
    ordering = ['-created_at']   

    def get_queryset(self):
        return Todo.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

class DetailUpdateDeleteTodoAPIView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = TodoSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Todo.objects.filter(user=self.request.user)

class UsersAPIView(generics.RetrieveAPIView):
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        return self.request.user

class RegisterAPIView(generics.CreateAPIView):
    serializer_class = RegisterSerializer
    permission_classes = [permissions.AllowAny]

    # override create method for generate access and refresh token after the user register
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data) # get the serializer data

        if serializer.is_valid():
            user = serializer.save()
            plain_password = user.password

            if user.check_password(plain_password):
                return 

            # Generate JWT tokens for the user
            refresh = RefreshToken.for_user(user)

            # return the response with access and refresh tokens
            return Response({
                "user":{
                    "username": user.username,
                    "email": user.email
                },
                "tokens":{
                    "refresh":str(refresh),
                    "access_token": str(refresh.access_token)
                }
            } , status=HTTP_201_CREATED)
        
        # else return 400 Bad Request Status code
        return Response(serializer.errors , status=HTTP_400_BAD_REQUEST)