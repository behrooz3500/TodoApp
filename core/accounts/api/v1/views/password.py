# dj
from django.contrib.auth import get_user_model

# rest
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status

# third party modules
import jwt
from jwt.exceptions import ExpiredSignatureError, InvalidSignatureError
from decouple import config

# account api
from ..serializers import (
    ChangePasswordSerializer,
    PasswordResetRequestSerializer,
    PasswordResetConfirmSerializer,
)
from ..utils import send_activation_email

User = get_user_model()


class PasswordChangeAPIView(generics.GenericAPIView):
    """ View for changing the password """
    permission_classes = [IsAuthenticated]
    serializer_class = ChangePasswordSerializer
    model = User

    def get_current_user(self, queryset=None):
        current_user = self.request.user
        return current_user

    def put(self, request, *args, **kwargs):
        self.current_user = self.get_current_user()
        serializer = self.serializer_class(
            data=request.data, context={'request': request}
        )

        serializer.is_valid(raise_exception=True)

        if not self.current_user.check_password(
                serializer.validated_data.get('old_password')):
            return Response(
                {"detail": "Old password is not correct"},
                status=status.HTTP_400_BAD_REQUEST
            )

        self.current_user.set_password(
            serializer.validated_data.get('new_password'))

        self.current_user.save()

        return Response(
            {'details': 'Password changed'},
            status=status.HTTP_200_OK
        )


class PasswordResetRequestAPIView(generics.GenericAPIView):
    """ Requesting for password reset based on email """
    serializer_class = PasswordResetRequestSerializer

    def post(self, request, *args, **kwargs):
        email_action = 'reset_password'
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        email = serializer.validated_data['email']
        user_object = serializer.validated_data['user_object']
        send_activation_email(user_object, email, email_action)
        return Response({'details': 'Reset password email sent successfully'})


class PasswordResetConfirmAPIView(generics.GenericAPIView):
    """ Resetting password with reset token """
    serializer_class = PasswordResetConfirmSerializer

    def put(self, request, token, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        try:
            decoded_token = jwt.decode(token, config('SECRET_KEY'), algorithms=["HS256"])
        except ExpiredSignatureError:
            return Response({'details': 'Token has been expired.'}, status=status.HTTP_400_BAD_REQUEST)
        except InvalidSignatureError:
            return Response({'details': 'Token is invalid'}, status=status.HTTP_400_BAD_REQUEST)
        except Exception:
            return Response({'details': 'Your token is not valid'}, status=status.HTTP_400_BAD_REQUEST)

        user_object = User.objects.get(pk=decoded_token.get('user_id'))
        serializer.is_valid(raise_exception=True)
        user_object.set_password(serializer.validated_data['password1'])
        user_object.save()
        return Response({'details': 'Password changed successfully'}, status=status.HTTP_200_OK)

