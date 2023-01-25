from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib.auth.decorators import login_required
from django.views.generic import View
from django.contrib.auth.mixins import LoginRequiredMixin
from abc import ABC, abstractmethod

from accounts.models import Profile
from accounts.forms import SignUpForm, ProfileEditForm


class BaseRegisterView(View, ABC):
    """Parent class for managing user authentication"""

    view_template_name: str
    view_form_class: type

    def __init__(self):
        self.template_name = self.view_template_name
        self.form_class = self.view_form_class

    def get(self, request):
        if not request.user.is_authenticated:
            form = self.form_class()
            context = {'form': form}
            return render(request, self.template_name, context=context)
        else:
            return redirect('/')

    @abstractmethod
    def post(self, request):
        pass


class SignupView(BaseRegisterView):
    """View for signing up new users"""

    view_template_name = 'accounts/signup.html'
    view_form_class = SignUpForm

    def post(self, request):
        form = self.form_class(request.POST)
        if form.is_valid():
            form.save()
            messages.add_message(request, messages.SUCCESS, "Signed up successfully!")
            return redirect('/accounts/login/')
        error = form.errors.as_data()
        for field in error:
            lists = [list(error[field][0])]
        messages.add_message(request, messages.ERROR, lists)
        return redirect('/accounts/signup')


class LoginView(BaseRegisterView):
    """View for user login using django's AuthenticationForm"""

    view_template_name = 'accounts/login.html'
    view_form_class = AuthenticationForm

    def post(self, request):
        form = self.form_class(request, data=request.POST)
        if form.is_valid():
            user = authenticate(
                request,
                username=form.cleaned_data['username'],
                password=form.cleaned_data['password'],
            )
            if user is not None:
                login(request, user)
                messages.add_message(request, messages.SUCCESS, f"Logged in as {request.user.email}")
                return redirect('/')
        error = form.errors.as_data()
        for field in error:
            lists = [list(error[field][0])]
        messages.add_message(request, messages.ERROR, lists)
        return render(request, self.template_name, context={'form': form})


class ProfileView(LoginRequiredMixin, View):
    """View for editing user profile"""

    def get(self, request):
        profile = Profile.objects.get(user=request.user)
        profile_content = {
            'username': profile.username,
            'first_name': profile.first_name,
            'last_name': profile.last_name,
            'birth_date': profile.birth_date,
            'image': profile.image,
        }
        form = ProfileEditForm(initial=profile_content)
        context = {'form': form}
        return render(request, template_name='profile.html', context=context)

    def post(self, request):
        old_profile = Profile.objects.get(user=request.user)
        form = ProfileEditForm(request.POST, request.FILES, instance=old_profile)
        if form.is_valid():
            form.save()
            messages.add_message(request, messages.SUCCESS, "Profile updated.")
            return redirect('/')
        messages.add_message(request, messages.ERROR, 'Invalid inputs!')
        return redirect('/accounts/profile')


@login_required()
def logout_view(request):
    """Logging out user"""

    if request.user.is_authenticated:
        logout(request)
        messages.add_message(request, messages.SUCCESS, 'Logged Out!')
        return redirect('/')


