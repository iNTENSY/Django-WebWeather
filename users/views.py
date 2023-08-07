from django.contrib.auth.views import LoginView
from django.shortcuts import redirect, render
from django.urls import reverse
from django.views import generic

from users import forms
from users.mixins import IsAuthenticatedMixin


class SignInView(IsAuthenticatedMixin, LoginView):
    form_class = forms.LoginForm
    template_name: str = 'users/login.html'

    def get_success_url(self):
        return reverse('weather:first_page')


class SignUpView(IsAuthenticatedMixin, generic.CreateView):
    form_class = forms.RegistrationForm
    template_name = 'users/registration.html'

    def get_success_url(self):
        return reverse('weather:first_page')


class ConfirmationView(generic.TemplateView):
    def get(self, request, *args, **kwargs):
        return render(self.request, 'payment/confirmation.html')
