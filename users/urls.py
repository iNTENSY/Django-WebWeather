from django.urls import path

from users import views

app_name = 'user'

urlpatterns = [
    path('login/', views.SignInView.as_view(), name='sign-in'),
    path('registration/', views.SignUpView.as_view(), name='sign-up'),
]