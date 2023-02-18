# dj
from django.contrib.auth.password_validation import validate_password
from django.core import exceptions
from django.contrib.auth import get_user_model

# rest
from rest_framework import serializers


User = get_user_model()


class RegistrationSerializer(serializers.ModelSerializer):
    """
    Serializer for managing registration data
    based on User model
    """

    password_confirm = serializers.CharField(max_length=255, write_only=True)

    class Meta:
        model = User
        fields = [
            "email",
            "password",
            "password_confirm",
        ]

    def validate(self, attrs):
        """Validating entered data for user registration"""
        if not attrs.get("password") == attrs.get("password_confirm"):
            raise serializers.ValidationError({"detail": "Password does not match"})

        try:
            validate_password(attrs.get("password"))
        except exceptions.ValidationError as e:
            raise serializers.ValidationError({"password": list(e.messages)})

        return super().validate(attrs)

    def create(self, validated_data):
        """Creating a user based on our custom UserManager class"""
        validated_data.pop("password_confirm", None)
        return User.objects.create_user(**validated_data)


class AccountResendTokenSerializer(serializers.Serializer):
    """Resending the activation link for an email"""

    email = serializers.EmailField(required=True)

    def validate(self, attrs):
        email = attrs.get("email")
        try:
            user_object = User.objects.get(email=email)
        except User.DoesNotExist:
            raise serializers.ValidationError({"detail": "User not found"})
        if user_object.is_verified:
            raise serializers.ValidationError({"detail": "User already verified"})
        attrs["user_object"] = user_object
        return super().validate(attrs)
