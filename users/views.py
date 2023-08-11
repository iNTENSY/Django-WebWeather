from typing import Any

from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView
from django.db.models import Max
from django.shortcuts import render
from django.urls import reverse, reverse_lazy
from django.utils.decorators import method_decorator
from django.views import generic
from django.views.decorators.cache import cache_page
from rest_framework.authtoken.models import Token

from users import forms
from users.forms import ProfileSettingsForm
from users.mixins import IsAuthenticatedMixin, RedirectToProfileMixin
from users.models import User
from weather.forms import FindCityForm


class SignInView(IsAuthenticatedMixin, LoginView):
    """
    Данный класс позволяет авторизоваться пользователям.
    """
    form_class = forms.LoginForm
    template_name: str = 'users/login.html'

    def get_success_url(self):
        return reverse('weather:first_page')


class SignUpView(IsAuthenticatedMixin, generic.CreateView):
    """
    Данный класс позволяет зарегистрироваться пользователям.
    """
    form_class = forms.RegistrationForm
    template_name = 'users/registration.html'

    def get_success_url(self):
        return reverse('weather:first_page')


@method_decorator(cache_page(60*5), name='dispatch')
class ProfileView(LoginRequiredMixin, RedirectToProfileMixin, generic.FormView):
    """
    Данный класс отображает страницу профиля пользователя исключительно для своего аккаунта.
    """
    form_class = FindCityForm
    template_name: str = 'users/profile.html'
    login_url = reverse_lazy('user:sign-in')

    def get_context_data(self, **kwargs) -> dict[str, Any]:
        context: dict[str, Any] = super().get_context_data()
        context['end_date'] = self.request.user.subscription.aggregate(Max('end_date'))['end_date__max']
        context['token'] = Token.objects.get(user=self.request.user).key
        return context


class ProfileSettingsView(LoginRequiredMixin, RedirectToProfileMixin, generic.TemplateView):
    """
    Данный класс отображает страницу с настройками (возможность смены пароля)
    исключительно для своего аккаунта.
    """
    template_name = 'users/settings.html'

    def get_context_data(self, *args, **kwargs):
        context: dict[str, Any] = super().get_context_data()
        context['form'] = FindCityForm
        context['settings_form'] = ProfileSettingsForm
        return context

    def get_success_url(self):
        return self.follow_to('profile')

    def post(self, *args, **kwargs):
        form = ProfileSettingsForm(self.request.POST)
        user = User.objects.get(username=self.request.user.username)
        if form.is_valid():
            if user.check_password(form.data['old_password']):
                user.set_password(form.data['new_password1'])
                user.save()
            return self.follow_to('profile')
        return self.follow_to('settings')


class ConfirmationView(generic.TemplateView):
    """
    Данный класс отображает статус платежа на странице.
    """
    def get(self, request, *args, **kwargs):
        return render(self.request, 'payment/confirmation.html')
