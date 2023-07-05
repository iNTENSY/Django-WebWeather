from django.urls import path

from .views import WeatherPageView, RedirectToView

app_name: str = 'weather'

urlpatterns = [
    path('', RedirectToView.as_view(), name='redirect'),
    path('weatherfinder/', WeatherPageView.as_view(), name='first_page'),
    path('weatherfinder/<str:city>', WeatherPageView.as_view(), name='page_for_find_city_by_name')
]