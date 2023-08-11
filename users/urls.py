from django.contrib.auth.views import LogoutView
from django.urls import path

from djangoWeather import settings
from users import views, payments

app_name = 'user'

urlpatterns = [
    path('login/', views.SignInView.as_view(), name='sign-in'),
    path('logout/', LogoutView.as_view(), {'next_page': settings.LOGOUT_REDIRECT_URL} ,name='logout'),
    path('registration/', views.SignUpView.as_view(), name='sign-up'),
    path('buy/', payments.PaymentView.as_view(), name='payment'),
    path('confirmation/', views.ConfirmationView.as_view(), name='confirmation'),
    path('profile/<int:pk>/', views.ProfileView.as_view(), name='profile'),
    path('profile/<int:pk>/settings/', views.ProfileSettingsView.as_view(), name='settings'),
]