import os
import requests
import logging
import pprint

logging.basicConfig(level=logging.DEBUG, format='%(asctime)s %(levelname)s %(message)s', datefmt='%d-%m-%y %H:%M:%S')
log = logging.getLogger('root')

# CONSTANT
WEATHER_KEY = os.environ.get('WEATHER_KEY')
API_URL = 'https://api.openweathermap.org/data/2.5/onecall?'


def main():
    if WEATHER_KEY is not None:
        # This lat and long should be passed from the program itself.
        lat, long = get_location()
        weather, errors = get_weather(lat, long)

        if weather is None:
            print('No forecast or invalid location......')
            # Add logger here?
        else:
            # parse the weather data here and then pass it back to the program
            weahter_data = store_data(weather)


def store_data(weather):
    pass


def get_location(lat=None, long=None):
    while lat is None:

        lat = input('Please enter the latitude of the location')

    while long is None:
        print('....')

    return lat, long


def get_weather(lat, long):
    params = {'lat': lat, 'lon': long, 'exclude': 'current,alerts,hourly,minutely', 'units': 'imperial',
              'appid': WEATHER_KEY}

    response = requests.get(API_URL, params=params)

    try:
        response.raise_for_status()
        data = response.json()
        return data, None

    except Exception as e:
        log.exception(f'Error occurred. More detail: {e}')
        log.exception(f'Error Message from request: {response.text}')
        return None, e



main()
