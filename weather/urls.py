from django.urls import path

from . import views

app_name: str = 'weather'

urlpatterns = [
    path('', views.RedirectToView.as_view(), name='redirect'),
    path('weatherfinder/', views.WeatherPageView.as_view(), name='first_page'),
    path('weatherfinder/ratings/', views.RatingView.as_view(), name='ratings'),
    path('weatherfinder/<str:city>/', views.WeatherPageView.as_view(), name='page_for_find_city_by_name'),
]