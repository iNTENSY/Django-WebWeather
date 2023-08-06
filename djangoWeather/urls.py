from django.contrib import admin
from django.urls import path, include

from weather import api
from .yasg import urlpatterns as doc_url

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('weather.urls', namespace='weather')),
    path('user/', include('users.urls', namespace='user')),
    path('api/auth/', include('djoser.urls')),
    path('api/auth/', include('djoser.urls.authtoken')),
    path('api/mostsearchedcity/', api.FrequentlySearchedAPIView.as_view()),
    path('api/notoftensearchedcity/', api.NotFrequentlySearchedAPIView.as_view()),
    path('api/getstatistic/<str:city>/', api.GetStatisticAPIView.as_view()),
    path('api/weatherdata/<str:city>/', api.WeatherDataAPIView.as_view()),
    path('api/moreweatherdata/<str:city>/', api.DetailWeatherDataAPIView.as_view()),
] + doc_url
