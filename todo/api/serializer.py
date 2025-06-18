from django.contrib.auth.models import User
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError
from rest_framework import serializers

from todo.models import Todo


class TodoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Todo
        fields = [
            'id',
            'title',
            'description',
            'completed',
            'created_at',
            'updated_at'
        ]

class UserSerializer(serializers.ModelSerializer):
    todos = TodoSerializer(many=True, read_only=True)  # علاقة عكسية

    class Meta:
        model = User
        fields = [
            'username',
            'email',
            'todos'
        ]

class RegisterSerializer(serializers.ModelSerializer):

    password = serializers.CharField(
        write_only = True,
        required=True,
        style={'input_type': 'password'}
    )

    confirm_password = serializers.CharField(
        write_only=True,
        required=True,
        style={'input_type': 'password'}
    )

    class Meta:
        model = User
        fields = [
            "username",
            "email",
            "password",
            "confirm_password"
        ]

    # validate the password strength
    def validate_password(self,value):
        try:
            validate_password(value)
        except ValidationError as e:
            raise serializers.ValidationError(e.messages)
        return value
    
    def validate(self, attrs):
        password = attrs.get("password")
        confirm_password = attrs.get("confirm_password")

        if password != confirm_password:
            raise serializers.ValidationError({
                "confirm_password":"Password do not match"
            })
        return attrs


    def create(self, validated_data):
        validated_data.pop('confirm_password')  # remove the confirm password field before saving
        user = User.objects.create_user(
            username=validated_data["username"],
            email= validated_data['email'],
            password=validated_data['password']
        )
        return user