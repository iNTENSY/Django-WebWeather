import os.path

import environ

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