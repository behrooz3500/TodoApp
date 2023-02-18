from django.urls import path, include

urlpatterns = [
    path("", include("accounts.api.v1.urls.user")),
    path("", include("accounts.api.v1.urls.profile")),
]
