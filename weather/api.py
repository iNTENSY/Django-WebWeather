from django.db.models import Max
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.throttling import UserRateThrottle, AnonRateThrottle, ScopedRateThrottle
from rest_framework.views import APIView

from weather.mixins import OpenWeatherMixin
from weather.models import Cities
from weather.serializers import CitySerializer


class FrequentlySearchedAPIView(APIView):
    throttle_classes = (UserRateThrottle, AnonRateThrottle)

    def get(self, request, *args, **kwargs) -> Response:
        """
        Данная функция возвращает из БД данные города(ов),
        который пользователи ищут чаще всего.
        Переменная max_searches означает самое большое число в
        строке модели total_searches из всех городов.
        """
        max_searches: int = Cities.objects.aggregate(Max('total_searches'))['total_searches__max']
        cities: Cities = Cities.objects.filter(total_searches=max_searches)
        serializer = CitySerializer(cities, many=True)
        return Response({'city': serializer.data})



class WeatherDataAPIView(OpenWeatherMixin, APIView):
    """
    Данный класс возвращает информацию по погоде на день
    в определенном городе.
    Класс использует ограниченное количество запросов в минуту.
    'anon': '5/min'
    'user': '7/min'
    """
    throttle_scope = 'user'

    def get(self, request, *args, **kwargs):
        response: dict = self.get_weatherdata_for_day(self.kwargs.get('city'))
        return Response(data=response)


class DetailWeatherDataAPIView(OpenWeatherMixin, APIView):
    """
    Данный класс основан на WeatherDataAPIView, при этом
    передает параметр True в WeatherDataAPIView.get(), а конкретнее
    в args. Таким образом возвращается детальная информация по погоде
    в городе с периодом в 3 часа.
    Данный класс может быть использован авторизованными пользователями,
    у которых также реализован лимит запросов в минуту.
    """
    permission_classes: tuple = (IsAuthenticated,)
    throttle_classes: list = []
    throttle_scope: str = 'premium'

    def get(self, request, *args, **kwargs):
        self.throttle_classes.append(ScopedRateThrottle if request.user.user_status == 'Premium' else UserRateThrottle)
        response: dict = self.get_weatherdata_every_3h(self.kwargs.get('city'))
        return Response(data=response)