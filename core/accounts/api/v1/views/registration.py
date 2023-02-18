# dj
from django.contrib.auth import get_user_model

# rest
from rest_framework import generics
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

# modules
import jwt
from decouple import config
from jwt.exceptions import ExpiredSignatureError, InvalidSignatureError

# account api
from ..serializers import RegistrationSerializer, AccountResendTokenSerializer
from ..utils import send_activation_email

User = get_user_model()


class RegistrationAPIView(generics.GenericAPIView):
    """View for registering users via api"""

    serializer_class = RegistrationSerializer

    def post(self, request, *args, **kwargs):
        email_action = "activation"
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        email = serializer.validated_data["email"]
        data = {
            "detail": "User created successfully.",
            "email": email,
        }
        user_object = User.objects.get(email=email)
        send_activation_email(user_object, email, email_action)

        return Response(data, status.HTTP_201_CREATED)


class AccountActivationAPIView(APIView):
    """View for account activation"""

    def get(self, request, token, *args, **kwargs):
        try:
            decoded_token = jwt.decode(
                token, config("SECRET_KEY"), algorithms=["HS256"]
            )
        except ExpiredSignatureError:
            return Response(
                {"details": "Token has been expired."},
                status=status.HTTP_400_BAD_REQUEST,
            )
        except InvalidSignatureError:
            return Response(
                {"details": "Token is invalid"}, status=status.HTTP_400_BAD_REQUEST
            )
        except Exception:
            return Response(
                {"details": "Your token is not valid"},
                status=status.HTTP_400_BAD_REQUEST,
            )
        user_object = User.objects.get(pk=decoded_token.get("user_id"))
        if user_object.is_verified:
            return Response(
                {"details": "Account was already verified"},
                status=status.HTTP_400_BAD_REQUEST,
            )
        user_object.is_verified = True
        user_object.save()
        return Response(
            {"details": "Your account has been verified successfully"},
            status=status.HTTP_200_OK,
        )


class AccountResendTokenAPIView(generics.GenericAPIView):
    """View for resending activation token"""

    serializer_class = AccountResendTokenSerializer

    def post(self, request, *arg, **kwargs):
        email_action = "activation"
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        email = serializer.validated_data["email"]
        user_object = serializer.validated_data["user_object"]
        send_activation_email(user_object, email, email_action)
        return Response({"details": "Activation email sent successfully"})
