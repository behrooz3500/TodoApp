# dj
from django.urls import path

# account api
from .. import views

# jwt
from rest_framework_simplejwt.views import (
    TokenRefreshView,
    TokenVerifyView,
)


# from drf_spectacular.views import SpectacularAPIView


urlpatterns = [
    path("registration/", views.RegistrationAPIView.as_view(), name="registration"),
    path("token/simple/login/", views.TokenLoginAPIView.as_view(), name="token-login"),
    path(
        "token/simple/logout/", views.TokenLogoutAPIView.as_view(), name="token-logout"
    ),
    path(
        "token/jwt/create/",
        views.CustomTokenObtainPairView.as_view(),
        name="token-create",
    ),
    path("token/jwt/refresh/", TokenRefreshView.as_view(), name="token-refresh"),
    path("token/jwt/verify/", TokenVerifyView.as_view(), name="token-verify"),
    path(
        "password/change/",
        views.PasswordChangeAPIView.as_view(),
        name="password-change",
    ),
    path(
        "password/reset/request/",
        views.PasswordResetRequestAPIView.as_view(),
        name="password-reset-request",
    ),
    path(
        "password/reset/<str:token>",
        views.PasswordResetConfirmAPIView.as_view(),
        name="password-reset",
    ),
    path("test-mail/", views.TestMailSender.as_view(), name="test-mail"),
    path(
        "activation/<str:token>",
        views.AccountActivationAPIView.as_view(),
        name="activation",
    ),
    path(
        "activation/resend/",
        views.AccountResendTokenAPIView.as_view(),
        name="resend-token",
    ),
    # path('schema/', SpectacularAPIView.as_view(), name='schema'),
]
