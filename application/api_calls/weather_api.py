import os
import requests
import logging
from dotenv import load_dotenv
from pprint import pprint
import re
from datetime import datetime
import cache
from ..models import List
import time

cached_time = 86400   #one day
load_dotenv('application/.env')

# Logger
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s %(levelname)s %(message)s', datefmt='%d-%m-%y %H:%M:%S')
log = logging.getLogger('root')

# CONSTANT
WEATHER_KEY = os.environ.get('WEATHER_KEY')

API_URL = 'https://api.openweathermap.org/data/2.5/onecall?'


def store_data(weather):
    weather_list = list()
    for day in weather['daily']:
        weather_dict = dict()
        dt_txt = datetime.fromtimestamp(day['dt']).strftime("%Y-%m-%d %I:%M:%S")

        date_string = re.search(r'\d{4}-\d{2}-\d{2}', dt_txt).group(0)
        weather_dict['date'] = date_string
        temp_list = day['temp']
        tmp_desc = day['weather']
        for i in tmp_desc:
            temp_desc = i['description']
        temp_humidity = day['humidity']
        weather_dict['temp'] = temp_list
        weather_dict['desc'] = temp_desc
        weather_dict['humidity'] = temp_humidity
        if 'rain' in day.keys():
            temp_rain = day['rain']
            weather_dict['rain'] = temp_rain
        weather_list.append(weather_dict)

    return weather_list



def get_weather(lat, lon):
    params = {'lat': lat, 'lon': lon, 'exclude': 'current,alerts,hourly,minutely', 'units': 'imperial',
              'appid': WEATHER_KEY}

    response = requests.get(API_URL, params=params)

    #see if weather_list is in cache; otherwise, do API call
    #identifier is lat/long
    cached_weather_list = cache.fetch((lat,lon))
    if cached_weather_list:
        log.info('Return from Cache')  
        return cached_weather_list
    else:
        log.info('new API call')
        try:
            response.raise_for_status()
            data = response.json()

            weather_list = store_data(data)
        #cache new weather_list for 1 day
            weather_list = List(weather_list, now_plus_expiry)
            #cache.add((lat,lon), weather_list)
            cache.add((lat,lon),weather_list)
            return weather_list
            
        except Exception as e:
            log.exception(f'Error occurred. More detail: {e}')
            log.exception(f'Error Message from request: {response.text}')
            raise e


def now_plus_expiry():
    now =time.time()
    return now + cached_time
