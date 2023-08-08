from django.urls import path

from users import views, payments

app_name = 'user'

urlpatterns = [
    path('login/', views.SignInView.as_view(), name='sign-in'),
    path('registration/', views.SignUpView.as_view(), name='sign-up'),
    path('buy/', payments.PaymentView.as_view(), name='payment'),
    path('confirmation/', views.ConfirmationView.as_view(), name='confirmation'),
    path('profile/<int:pk>/', views.ProfileView.as_view(), name='profile'),
]