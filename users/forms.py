from django import forms
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm

from users.models import User


class LoginForm(AuthenticationForm):
    username = forms.CharField(widget=forms.TextInput(
        attrs={
            'type': 'text',
            'class': 'form-control',
            'id': 'floatingInput',
            'placeholder': 'Your username'
        }
    ))
    password = forms.CharField(widget=forms.PasswordInput(
        attrs={
            'type': 'password',
            'class': 'form-control',
            'id': 'floatingPassword',
            'placeholder': 'Password'
        }
    ))

    class Meta:
        model: User = User
        fields: tuple[str] = ('username', 'password')


class RegistrationForm(UserCreationForm):
    username = forms.CharField(widget=forms.TextInput(
        attrs={
            'type': 'text',
            'class': 'form-control mb-1',
            'id': 'floatingInput',
            'placeholder': 'Your username'
        }
    ))
    password1 = forms.CharField(widget=forms.PasswordInput(
        attrs={
            'type': 'password',
            'class': 'form-control mb-1',
            'id': 'floatingPassword1',
            'placeholder': 'Password'
        }
    ))
    password2 = forms.CharField(widget=forms.PasswordInput(
        attrs={
            'type': 'password',
            'class': 'form-control mb-1',
            'id': 'floatingPassword2',
            'placeholder': 'Repeat password'
        }
    ))

    class Meta:
        model: User = User
        fields: tuple[str] = ('username', 'password1', 'password2')