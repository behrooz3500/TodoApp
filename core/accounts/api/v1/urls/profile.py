# dj
from django.urls import path

# account api
from .. import views

urlpatterns = [
    path('profile/', views.ProfileAPIView.as_view(), name='profile'),
]
