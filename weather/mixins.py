import os.path

import environ
import requests

from djangoWeather.settings import BASE_DIR


env = environ.Env()
env.read_env(os.path.join(BASE_DIR), '.env')

class UrlMixin:
    """
    Данный миксин используется для обозначения стандартных констант поиска.
    """
    FIND_CITY_BY_IP_URL: str = 'http://ip-api.com/json/{}?lang=ru'
    OPENWEATHERMAP_URL: str = ('https://api.openweathermap.org/data/2.5/'
                               'weather?q={}&units=metric&lang=ru&app'
                               f'id={env.str("WEATHER_APP_ID")}')
    MORE_DATA_OPENWEATHERMAP_URL: str = (
        'https://api.openweathermap.org/data/2.5'
        f'/forecast?appid={env.str("WEATHER_APP_ID")}&'
        'lang=ru&q={}')


class OpenWeatherMixin(UrlMixin):
    """
    Данный миксин используется для получения данных погоды
    в одном из городов с возможностью узнать
    через каждые 3 часа или на целый день.
    """
    DEFAULT_EXCEPTION: dict[str, str]  = {
                'city': 'Данного города не существует или вы ввели неверные данные.'
            }

    def get_weatherdata_for_day(self, city: str = None) -> dict:
        url: str = self.OPENWEATHERMAP_URL.format(city)
        response: dict = self.try_to_get(url)
        return response

    def get_weatherdata_every_3h(self, city: str = None) -> dict:
        url: str = self.MORE_DATA_OPENWEATHERMAP_URL.format(city)
        response: dict = self.try_to_get(url)
        return response

    def try_to_get(self, url: str) -> dict:
        try:
            response = requests.get(url).json()
            if response['cod'] == '404':
                raise ValueError
        except ValueError:
            response = self.DEFAULT_EXCEPTION
        return response
