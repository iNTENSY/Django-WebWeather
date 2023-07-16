from django.contrib import admin
from django.urls import path, include

from weather import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('weather.urls', namespace='weather')),
    path('api/mostsearchedcity/', views.FrequentlySearchedAPIView.as_view()),
    path('api/weatherdata/<str:city>/', views.WeatherDataAPIView.as_view()),
    path('api/moreweatherdata/<str:city>/', views.DetailWeatherDataAPIView.as_view()),
]
