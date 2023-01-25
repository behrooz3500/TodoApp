from django import forms
from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model
from accounts.models import Profile

User = get_user_model()


class SignUpForm(UserCreationForm):
    """Form used for registering new users with email"""
    email = forms.EmailField(max_length=255)

    class Meta:
        model = User
        fields = ['email', 'password1', 'password2']

    def __init__(self, *args, **kwargs):
        super(UserCreationForm, self).__init__(*args, **kwargs)
        for fieldname in ['email', 'password1', 'password2']:
            self.fields[fieldname].help_text = None


class ProfileEditForm(ModelForm):
    """Form used for editing user profile"""
    class Meta:
        model = Profile
        fields = ['username', 'first_name', 'last_name', 'birth_date', 'image', ]
        widgets = {
            'birth_date': forms.DateInput(
                                          attrs={'class': 'form-control', 'placeholder': 'Select a date',
                                                 'type': 'date'}),
        }
