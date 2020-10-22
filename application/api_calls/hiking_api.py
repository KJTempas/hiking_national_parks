import requests
import os
import logging
from dotenv import load_dotenv

from cache import cache, cache_list
from datetime import datetime
import time

cached_time = 26280000

load_dotenv('application/.env')

HIKING_KEY = os.environ.get('HIKING_KEY')
HIKING_URL = 'https://www.hikingproject.com/data/get-trails'

# Logger
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s %(levelname)s %(message)s', datefmt='%d-%m-%y %H:%M:%S')
log = logging.getLogger('root')


def get_trails(lat, lon):

    # see if trail_list is in cache; otherwise, do API call
    # identifier is lat/long
    cached_trail_list = cache.fetch((lat, lon), cache_list.DataList)
    if cached_trail_list:
        log.info('Return from Cache')  # this will be deleted later
        return cached_trail_list
    else:
        log.info('new API call')

        try:
            query = {'lat': lat, 'lon': lon, 'key': HIKING_KEY}

            response = requests.get(HIKING_URL, params=query)
            response.raise_for_status()  # will raise an exception for 400(client) or 500(server) errors
            data = response.json()
            trail_list = list()
            list_of_trails = data['trails']


            if list_of_trails:
                for trail in list_of_trails:
                    trail_list_w_info = dict()
                    if trail['name'] and trail['length'] and trail['difficulty'] and trail['summary'] :

                        trail_list_w_info['name'] = trail['name']
                        trail_list_w_info['length'] = trail['length']
                        trail_list_w_info['difficulty'] = trail['difficulty']
                        trail_list_w_info['summary'] = trail['summary']

                        trail_list.append(trail_list_w_info)


        # for x in range(-1, 5):
        #     trail_name = data['trails'][x]['name']
        #     trail_summary = data['trails'][x]['summary']
        #     trail_length = data['trails'][x]['length']
        #     trail_difficulty = data['trails'][x]['difficulty']
        #     trail_img = data['trails'][x]['imgMedium']
        #     trail_list.append(trail_name)
        #     #
        # print(
        #     f'Name: {trail_name} | Trail summary: {trail_summary} | Trail length: {trail_length} | Trail difficulty: {trail_difficulty} | Trail img: {trail_img}')
 
            #add data to cache - expires in 1 month
            hiking_trails_data_list_for_cache = cache_list.DataList(trail_list, (lat,lon), now_plus_expiry)
            cache.add(hiking_trails_data_list_for_cache)

            return trail_list
        except Exception as e:
            log.exception(e)
            raise e


def now_plus_expiry():
    now = int(time.time())
    return now + cached_time
