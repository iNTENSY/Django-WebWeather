from typing import Any

from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView
from django.shortcuts import redirect, render
from django.urls import reverse, reverse_lazy
from django.views import generic
from rest_framework.authtoken.models import Token

from users import forms
from users.mixins import IsAuthenticatedMixin
from users.models import User


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


class ProfileView(LoginRequiredMixin, generic.DetailView):
    model = User
    context_object_name: str = 'profile'
    template_name: str = 'users/profile.html'
    login_url = reverse_lazy('user:sign-in')

    def get(self, request, *args, **kwargs):
        if self.request.user.pk != self.kwargs.get('pk'):
            return redirect(reverse('user:profile', kwargs={'pk': self.request.user.pk}))
        return super(ProfileView, self).get(request, *args, **kwargs)

    def get_context_data(self, **kwargs) -> dict[str, Any]:
        context: dict[str, Any] = super().get_context_data()
        context['token'] = Token.objects.get(user=self.request.user)
        return context

class ConfirmationView(generic.TemplateView):
    def get(self, request, *args, **kwargs):
        return render(self.request, 'payment/confirmation.html')
