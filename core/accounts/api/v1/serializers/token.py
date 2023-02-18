# dj
from django.utils.translation import gettext_lazy as _
from django.contrib.auth import authenticate, get_user_model

# rest
from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer


User = get_user_model()


class TokenSerializer(serializers.Serializer):
    email = serializers.EmailField(label=_("Email"), write_only=True)
    password = serializers.CharField(
        label=_("Password"),
        style={"input_type": "password"},
        trim_whitespace=False,
        write_only=True,
    )
    token = serializers.CharField(label=_("Token"), read_only=True)

    def validate(self, attrs):
        username = attrs.get("email")
        password = attrs.get("password")

        if username and password:
            user = authenticate(
                request=self.context.get("request"),
                username=username,
                password=password,
            )

            # Authenticate call simply returns None for is_active=False
            # users. (Assuming the default ModelBackend authentication
            # backend.)
            if not user:
                msg = _("Unable to log in with provided credentials.")
                raise serializers.ValidationError(msg, code="authorization")
            if not user.is_verified:
                raise serializers.ValidationError({"details": "User is not verified"})
        else:
            msg = _('Must include "email" and "password".')
            raise serializers.ValidationError(msg, code="authorization")

        attrs["user"] = user
        return attrs


class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    """Custom serializer to include additional attributes"""

    def validate(self, attrs):
        validated_data = super().validate(attrs)
        if not self.user.is_verified:
            raise serializers.ValidationError({"details": "User is not verified"})
        validated_data["email"] = self.user.email
        return validated_data
