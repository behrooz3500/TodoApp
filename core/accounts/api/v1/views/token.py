# dj
from django.contrib.auth import get_user_model

# rest
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token

# jwt
from rest_framework_simplejwt.views import TokenObtainPairView


# account api
from ..serializers import (
    TokenSerializer,
    CustomTokenObtainPairSerializer,
)


User = get_user_model()


class TokenLoginAPIView(ObtainAuthToken):
    """ Custom class for logging based on a generated token """
    serializer_class = TokenSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data,
                                           context={'request': request})
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        token, created = Token.objects.get_or_create(user=user)
        return Response({
            'token': token.key,
            'user_id': user.pk,
            'email': user.email
        })


class TokenLogoutAPIView(APIView):
    """ Logging out and discarding current token """
    permission_classes = [IsAuthenticated]

    def post(self, request):
        request.user.auth_token.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class CustomTokenObtainPairView(TokenObtainPairView):
    """ Custom class for jwt token creation """
    serializer_class = CustomTokenObtainPairSerializer



