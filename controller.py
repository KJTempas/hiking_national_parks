#import 
import cache
from model import Trails #whatever Quinn called the model
from datetime import datetime
import time


def get_hiking_info(trail):
    cached_time = 604800 #sec = 1 wk
    if cached_hiking_info := cache.fetch(trail_number, TrailList):
        print('Returned from cache')
        return cached_trail_list
    
    else:
        #make a new API call for fresh data
        print('Made a new API call')
        trail_info = api_calls_hiking_api.get_hiking_info(lat, longitude)

        cache.add(trail_info_list)
        return trail_info_list
    
def get_weather_info(lat,long):
    cached_time = 3600 #3600 sec = 1 hour
    #if cached weather is in time frame, return it
    if cached_weather_info:= cache.fetch(weather, ??):
        print('Returned from cache')
        return cached_weather

    else: #make a new call to the API
        print('Made new API call')
        updated_weather = api_calls.weather_api.get_weather_by_location(lat,longitude):
        cache.add(updated_weather)
        return updated_weather


def now_plus_expiry(): #this method calculates times since data was put in cache
    now = time.time()
    return now + cached_time