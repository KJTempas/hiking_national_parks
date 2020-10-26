import unittest
from unittest import TestCase
from unittest.mock import patch #maybe not needed

import api_calls

from api_calls import weather_api

class TestWeatherAPI(TestCase):
    def test_retrieve_weather_info_no_rain(self):
        example_api_response = {
       # {"lat":65.96,"lon":-164.41,"timezone":"America/Nome","timezone_offset":-28800,
        "daily":
        [{"dt":1603663200,"sunrise":1603650614,"sunset":1603680765,
        "temp":{"day":30.99,"min":30.36,"max":31.55,"night":30.42,"eve":31.03,
        "morn":30.61},"feels_like":{"day":22.24,"night":20.46,"eve":22.71,"morn":23.04},
        "pressure":1014,"humidity":98,"dew_point":30.56,"wind_speed":8.79,"wind_deg":48,
        "weather":[{"id":804,"main":"Clouds","description":"overcast clouds","icon":"04d"}],
        "clouds":100,"pop":0.07,"uvi":0.26},

        {"dt":1603749600,"sunrise":1603737225,"sunset":1603766944,
        "temp":{"day":29.97,"min":26.82,"max":30.34,"night":30.33,"eve":30.34,
        "morn":28.51},"feels_like":{"day":17.35,"night":21.09,"eve":19.67,
        "morn":21.52},"pressure":1006,"humidity":95,"dew_point":25.61,
        "wind_speed":15.26,"wind_deg":307,"weather":[{"id":804,"main":"Clouds",
        "description":"overcast clouds","icon":"04d"}],"clouds":88,"pop":0.4,"uvi":0.27}]}
         #}
        
        #expected response = list of dictionaries
        expected_weather_list = [
            {"date": "2020-10-25",
            "temp":{"day:30.99","min:30.36","max:31.55","night:30.42","eve:31.03",
                "morn:30.61"},
            # ["min": 30.36, "max":31.55],
            "desc": "overcast clouds",
            "humidity": 98},
            #"rain": ''},#rain not in list since no rain in forecast

            {"date": "2020-10-26",
            "temp":{"day:29.97","min:26.82","max:30.34","night:30.33","eve:30.34",
                "morn:28.51"},
           # "temp": ["min":26.82, "max":30.34],
            "desc": "overcast clouds",
            "humidity": 95}
            #"rain": ''} 
        ]

        weather_list = api_calls.weather_api.store_data(example_api_response)
        #compare data
        self.assertEqual(expected_weather_list, weather_list)
    
#TODO another test with rain included
  #  def test_retrieve_weather_info_with_rain(self):