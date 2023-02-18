# dj
from django.contrib.auth.password_validation import validate_password
from django.core import exceptions
from django.contrib.auth import get_user_model

# rest
from rest_framework import serializers


User = get_user_model()


class ChangePasswordSerializer(serializers.Serializer):
    """Serializer for changing the password"""

    old_password = serializers.CharField(max_length=255, required=True, write_only=True)
    new_password = serializers.CharField(max_length=255, required=True, write_only=True)
    new_password1 = serializers.CharField(
        max_length=255, required=True, write_only=True
    )

    def validate(self, attrs):
        PASSWORD_NOT_MATCH = "Password does not match"
        PASSWORD_NOT_NEW = "Enter a new password"
        if not attrs.get("new_password") == attrs.get("new_password1"):
            raise serializers.ValidationError({"detail": PASSWORD_NOT_MATCH})
        if attrs.get("new_password") == attrs.get("old_password"):
            raise serializers.ValidationError({"detail": PASSWORD_NOT_NEW})

        try:
            validate_password(attrs.get("new_password"))
        except exceptions.ValidationError as e:
            raise serializers.ValidationError({"password": list(e.messages)})

        return super().validate(attrs)


class PasswordResetRequestSerializer(serializers.Serializer):
    """Request a password reset with email"""

    email = serializers.EmailField(required=True)

    def validate(self, attrs):
        email = attrs.get("email")
        try:
            user_object = User.objects.get(email=email)
        except User.DoesNotExist:
            raise serializers.ValidationError({"detail": "Email not found"})
        attrs["user_object"] = user_object
        return super().validate(attrs)


class PasswordResetConfirmSerializer(serializers.Serializer):
    """Resetting the password"""

    password1 = serializers.CharField(required=True)
    password2 = serializers.CharField(required=True)

    def validate(self, attrs):
        password1 = attrs.get("password1")
        password2 = attrs.get("password2")

        if not password1 == password2:
            raise serializers.ValidationError({"details": "Passwords do not match"})

        try:
            validate_password(password1)
        except exceptions.ValidationError as e:
            raise serializers.ValidationError({"password": list(e.messages)})

        attrs.pop("password2")
        return super().validate(attrs)
