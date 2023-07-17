import os.path

import environ
import requests

from djangoWeather.settings import BASE_DIR


env = environ.Env()
env.read_env(os.path.join(BASE_DIR), '.env')

class UrlMixin:
    FIND_CITY_BY_IP_URL: str = 'http://ip-api.com/json/{}?lang=ru'
    OPENWEATHERMAP_URL: str = ('https://api.openweathermap.org/data/2.5/'
                               'weather?q={}&units=metric&lang=ru&app'
                               f'id={env.str("WEATHER_APP_ID")}')
    MORE_DATA_OPENWEATHERMAP_URL: str = (
        'https://api.openweathermap.org/data/2.5'
        f'/forecast?appid={env.str("WEATHER_APP_ID")}&'
        'lang=ru&q={}')


class OpenWeatherMixin(UrlMixin):
    def get_weatherdata_for_day(self, city: str = None):
        try:
            url: str = self.OPENWEATHERMAP_URL.format(city)
            response = requests.get(url).json()
            if response['cod'] == '404':
                raise ValueError
        except ValueError:
            response = {
                'city': 'Данного города не существует или вы ввели неверные данные.'
            }
        return response

    def get_weatherdata_every_3h(self, city: str = None):
        try:
            url: str = self.MORE_DATA_OPENWEATHERMAP_URL.format(city)
            response = requests.get(url).json()
            if response['cod'] == '404':
                raise ValueError
        except ValueError:
            response = {
                'city': 'Данного города не существует или вы ввели неверные данные.'
            }
        return response