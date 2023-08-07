from django.shortcuts import redirect
from django.urls import reverse


class IsAuthenticatedMixin:
    def get(self, request, *args, **kwargs):
        if self.request.user.is_authenticated:
            return redirect(reverse('weather:first_page'))
        return super().get(request, *args, **kwargs)