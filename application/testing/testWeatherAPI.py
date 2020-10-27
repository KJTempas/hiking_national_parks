import unittest
from unittest import TestCase
from unittest.mock import patch #maybe not needed

import api_calls

from api_calls import weather_api

class TestWeatherAPI(TestCase):
    def test_retrieve_weather_info_no_rain(self):
        example_api_response =  {'lat': 34.33, 'lon': -88.71, 'timezone': 'America/Chicago', 
            'timezone_offset': -18000, 'daily': [{'dt': 1603731600, 'sunrise': 1603714189, 
            'sunset': 1603753646, 'temp': {'day': 66.54, 'min': 49.42, 'max': 68.94, 'night': 59.2, 
            'eve': 59.97, 'morn': 49.42}, 'feels_like': {'day': 65.79, 'night': 54.91, 'eve': 57.36, 
            'morn': 46.27}, 'pressure': 1019, 'humidity': 70, 'dew_point': 56.5, 'wind_speed': 4.92, 
            'wind_deg': 31, 'weather': [{'id': 803, 'main': 'Clouds', 'description': 'broken clouds',
             'icon': '04d'}], 'clouds': 59, 'pop': 0, 'uvi': 4.68}, {'dt': 1603818000, 
             'sunrise': 1603800642, 'sunset': 1603839983, 'temp': {'day': 71.92, 'min': 52.74, 
             'max': 75.04, 'night': 65.28, 'eve': 65.8, 'morn': 52.74}, 'feels_like': {'day': 70.93, 
             'night': 62.92, 'eve': 62.76, 'morn': 48.67}, 'pressure': 1020, 'humidity': 66,
              'dew_point': 60.24, 'wind_speed': 7.52, 'wind_deg': 46, 'weather': [{'id': 801, 
              'main': 'Clouds', 'description': 'few clouds', 'icon': '02d'}], 'clouds': 17, 'pop': 0, 
              'uvi': 4.49}, {'dt': 1603904400, 'sunrise': 1603887096, 'sunset': 1603926321, 
              'temp': {'day': 72.52, 'min': 63.41, 'max': 72.52, 'night': 70.11, 'eve': 69.67, 
              'morn': 66.47}, 'feels_like': {'day': 75.78, 'night': 70.29, 'eve': 72.48, 'morn': 68.59}, 
              'pressure': 1013, 'humidity': 92, 'dew_point': 70.3, 'wind_speed': 7.81, 'wind_deg': 124,
               'weather': [{'id': 502, 'main': 'Rain', 'description': 'heavy intensity rain', 'icon': '10d'}],
                'clouds': 100, 'pop': 1, 'rain': 42.88, 'uvi': 4.57}, {'dt': 1603990800, 'sunrise': 1603973551, 
                'sunset': 1604012661, 'temp': {'day': 66.31, 'min': 53.56, 'max': 70.2, 'night': 53.56, 'eve': 54.63, 
                'morn': 68.97}, 'feels_like': {'day': 58.75, 'night': 46.45, 'eve': 45.97, 'morn': 72.09},
                 'pressure': 1005, 'humidity': 61, 'dew_point': 52.92, 'wind_speed': 14.79, 'wind_deg': 248, 
                 'weather': [{'id': 501, 'main': 'Rain', 'description': 'moderate rain', 'icon': '10d'}], 
                 'clouds': 66, 'pop': 1, 'rain': 5.21, 'uvi': 4.17}, {'dt': 1604077200, 'sunrise': 1604060006, 
                 'sunset': 1604099001, 'temp': {'day': 57.06, 'min': 47.48, 'max': 58.14, 'night': 47.48, 'eve': 50.38, 
                 'morn': 51.13}, 'feels_like': {'day': 49.46, 'night': 41.52, 'eve': 44.38, 'morn': 43.29}, 
                 'pressure': 1023, 'humidity': 62, 'dew_point': 44.56, 'wind_speed': 11.07, 'wind_deg': 7, 
                 'weather': [{'id': 802, 'main': 'Clouds', 'description': 'scattered clouds', 'icon': '03d'}], 
                 'clouds': 39, 'pop': 0, 'uvi': 4.14}, {'dt': 1604163600, 'sunrise': 1604146461, 'sunset': 1604185343, 'temp': {'day': 64.92, 'min': 42.19, 'max': 66.7, 'night': 56.14, 'eve': 58.06, 'morn': 42.19}, 'feels_like': {'day': 61.11, 'night': 54.95, 'eve': 57.25, 'morn': 36.64}, 'pressure': 1023, 'humidity': 63, 'dew_point': 52.3, 'wind_speed': 7.92, 'wind_deg': 157, 'weather': [{'id': 801, 'main': 'Clouds', 'description': 'few clouds', 'icon': '02d'}], 'clouds': 21, 'pop': 0, 'uvi': 4.21}, {'dt': 1604250000, 'sunrise': 1604232916, 'sunset': 1604271686, 'temp': {'day': 67.87, 'min': 53.17, 'max': 67.87, 'night': 53.17, 'eve': 56.5, 'morn': 57.7}, 'feels_like': {'day': 65.91, 'night': 47.1, 'eve': 50.83, 'morn': 57.69}, 'pressure': 1024, 'humidity': 59, 'dew_point': 53.33, 'wind_speed': 5.14, 'wind_deg': 331, 'weather': [{'id': 803, 'main': 'Clouds', 'description': 'broken clouds', 'icon': '04d'}], 'clouds': 71, 'pop': 0, 'uvi': 3.94}, {'dt': 1604336400, 'sunrise': 1604319372, 'sunset': 1604358030, 'temp': {'day': 61.3, 'min': 42.33, 'max': 62.92, 'night': 48.13, 'eve': 51.62, 'morn': 42.33}, 'feels_like': {'day': 55.06, 'night': 43.3, 'eve': 46.36, 'morn': 35.55}, 'pressure': 1028, 'humidity': 48, 'dew_point': 41.58, 'wind_speed': 7.65, 'wind_deg': 26, 'weather': [{'id': 800, 'main': 'Clear', 'description': 'clear sky', 'icon': '01d'}], 'clouds': 0, 'pop': 0, 'uvi': 3.8}]}



       
        expected_weather_list = [{'date': '2020-10-26', 'temp': {'day': 66.54, 'min': 49.42, 'max': 68.94, 'night': 59.2, 'eve': 59.97, 'morn': 49.42}, 'desc': 'Broken Clouds', 'humidity': 70}, {'date': '2020-10-27', 'temp': {'day': 71.92, 'min': 52.74, 'max': 75.04, 'night': 65.28, 'eve': 65.8, 'morn': 52.74}, 'desc': 'Few Clouds', 'humidity': 66}, {'date': '2020-10-28', 'temp': {'day': 72.52, 'min': 63.41, 'max': 72.52, 'night': 70.11, 'eve': 69.67, 'morn': 66.47}, 'desc': 'Heavy Intensity Rain', 'humidity': 92, 'rain': 42.88}, {'date': '2020-10-29', 'temp': {'day': 66.31, 'min': 53.56, 'max': 70.2, 'night': 53.56, 'eve': 54.63, 'morn': 68.97}, 'desc': 'Moderate Rain', 'humidity': 61, 'rain': 5.21}, {'date': '2020-10-30', 'temp': {'day': 57.06, 'min': 47.48, 'max': 58.14, 'night': 47.48, 'eve': 50.38, 'morn': 51.13}, 'desc': 'Scattered Clouds', 'humidity': 62}, {'date': '2020-10-31', 'temp': {'day': 64.92, 'min': 42.19, 'max': 66.7, 'night': 56.14, 'eve': 58.06, 'morn': 42.19}, 'desc': 'Few Clouds', 'humidity': 63}, {'date': '2020-11-01', 'temp': {'day': 67.87, 'min': 53.17, 'max': 67.87, 'night': 53.17, 'eve': 56.5, 'morn': 57.7}, 'desc': 'Broken Clouds', 'humidity': 59}, {'date': '2020-11-02', 'temp': {'day': 61.3, 'min': 42.33, 'max': 62.92, 'night': 48.13, 'eve': 51.62, 'morn': 42.33}, 'desc': 'Clear Sky', 'humidity': 48}]

        weather_list = api_calls.weather_api.store_data(example_api_response)
       
        #compare data
        self.assertEqual(expected_weather_list, weather_list)
    
#TODO another test with rain included
  #  def test_retrieve_weather_info_with_rain(self):