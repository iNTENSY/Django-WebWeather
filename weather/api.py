from django.db.models import Max, Min
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.throttling import UserRateThrottle, AnonRateThrottle, ScopedRateThrottle
from rest_framework.views import APIView

from weather.mixins import OpenWeatherMixin
from weather.models import Cities
from weather.serializers import CitySerializer


class FrequentlySearchedAPIView(APIView):
    throttle_classes = (UserRateThrottle, AnonRateThrottle)

    @method_decorator(cache_page(60))
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
    Данный класс может быть использован анонимными пользователями,
    у которых реализован лимит запросов.
    Данный класс может быть использован премиум-пользователями, у которых
    реализован свой лимит запросов.
    """
    throttle_classes: list = []

    def get(self, request, *args, **kwargs) -> Response:
        self.throttle_classes.append(
            AnonRateThrottle if request.user.is_anonymous else UserRateThrottle
        )
        response: dict = self.get_weatherdata_for_day(self.kwargs.get('city'))
        return Response(data=response)


class DetailWeatherDataAPIView(OpenWeatherMixin, APIView):
    """
    Данный класс использует OpenWeatherMixin для возврата детальной информации
    по погоде через каждые 3 часа.
    Данный класс может быть использован авторизованными пользователями,
    у которых реализован лимит запросов.
    Данный класс может быть использован премиум-пользователями, у которых
    реализован свой лимит запросов.
    """
    permission_classes: tuple = (IsAuthenticated,)
    throttle_classes: list = []
    throttle_scope: str = 'premium'

    def get(self, request, *args, **kwargs) -> Response:
        self.throttle_classes.append(
            ScopedRateThrottle if request.user.user_status == 'Premium' else UserRateThrottle
        )
        response: dict = self.get_weatherdata_every_3h(self.kwargs.get('city'))
        return Response(data=response)


class NotFrequentlySearchedAPIView(APIView):
    throttle_classes = (UserRateThrottle, AnonRateThrottle)

    @method_decorator(cache_page(60))
    def get(self, request, *args, **kwargs) -> Response:
        """
        Данная функция возвращает из БД данные города(ов),
        который пользователи не ищут чаще всего.
        Переменная min_searches означает самое минимальное число в
        строке модели total_searches из всех городов.
        """
        min_searches: int = Cities.objects.aggregate(Min('total_searches'))['total_searches__min']
        cities: Cities = Cities.objects.filter(total_searches=min_searches)
        serializer = CitySerializer(cities, many=True)
        return Response({'city': serializer.data})


class GetStatisticAPIView(APIView):
    @method_decorator(cache_page(60))
    def get(self, request, *args, **kwargs) -> Response:
        """
        """
        try:
            city: Cities = Cities.objects.get(name=self.kwargs['city'])
        except Cities.DoesNotExist:
            return Response({'city': f'Для города "{self.kwargs["city"]}" данных нет.'})
        serializer = CitySerializer(city)
        return Response({'city': serializer.data})