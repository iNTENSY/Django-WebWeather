from django.shortcuts import redirect
from django.urls import reverse


class IsAuthenticatedMixin:
    """
    При выполнении проверяется авторизован ли пользователь или нет.
    Если он уже авторизован, то будет перенаправлен на начальную страницу.
    """
    def get(self, request, *args, **kwargs):
        if self.request.user.is_authenticated:
            return redirect(reverse('weather:first_page'))
        return super().get(request, *args, **kwargs)


class RedirectToProfileMixin:
    """
    При выполнении используется метод get(), который
    перенаправляет на свою страницу, если идентификатор аккаунта (pk) в пути не совпадает
    с пользовательским.

    Метод follow_to() используется для сокращения, при перенаправлении
    """
    def follow_to(self, to: str):
        redirect_url = redirect(reverse(f'user:{to}', kwargs={'pk': self.request.user.pk}))
        return redirect_url

    def get(self, *args, **kwargs):
        if self.request.user.pk != self.kwargs.get('pk'):
            return self.follow_to(to='profile')
        return super().get(self.request, *args, **kwargs)