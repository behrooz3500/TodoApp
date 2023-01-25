from django.urls import path
from accounts.views import LoginView, logout_view, ProfileView, SignupView


app_name = 'accounts'


urlpatterns = [
    # login
    path('accounts/login/', LoginView.as_view(), name='login'),
    # logout
    path('accounts/logout/', logout_view, name='logout'),
    # registration
    path('accounts/signup', SignupView.as_view(), name='signup'),
    path('accounte/profile', ProfileView.as_view(), name='profile'),

]