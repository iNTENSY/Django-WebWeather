from django.contrib.auth.views import LoginView
from django.shortcuts import redirect, render
from django.urls import reverse_lazy, reverse
from django.views import generic, View

from users import forms


class SignInView(LoginView):
    form_class = forms.LoginForm
    template_name: str = 'users/login.html'

    def get_success_url(self):
        return reverse('weather:first_page')


class SignUpView(generic.CreateView):
    form_class = forms.RegistrationForm
    template_name = 'users/registration.html'

    def get_success_url(self):
        return reverse('weather:first_page')

    def get(self, request, *args, **kwargs):
        if self.request.user.is_authenticated:
            return redirect(reverse('weather:first_page'))
        return super(SignUpView, self).get(request, *args, **kwargs)


class ConfirmationView(generic.TemplateView):
    def get(self, request, *args, **kwargs):
        print(f'{kwargs=}')
        print(f'{args=}')
        return render(self.request, 'payment/confirmation.html')
