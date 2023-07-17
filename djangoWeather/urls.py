from django.contrib import admin
from django.urls import path, include

from weather import api

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('weather.urls', namespace='weather')),
    path('api/mostsearchedcity/', api.FrequentlySearchedAPIView.as_view()),
    path('api/weatherdata/<str:city>/', api.WeatherDataAPIView.as_view()),
    path('api/moreweatherdata/<str:city>/', api.DetailWeatherDataAPIView.as_view()),
]
