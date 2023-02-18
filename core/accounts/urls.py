from django.urls import path, include
from accounts.views import LoginView, logout_view, ProfileView, SignupView


app_name = "accounts"


urlpatterns = [
    path("login/", LoginView.as_view(), name="login"),
    path("logout/", logout_view, name="logout"),
    path("signup", SignupView.as_view(), name="signup"),
    path("profile", ProfileView.as_view(), name="profile"),
    path("api/v1/", include("accounts.api.v1.urls")),
]
