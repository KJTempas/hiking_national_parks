import os
import requests
import logging
from dotenv import load_dotenv
import html

from cache import cache, cache_list
from datetime import datetime
import time

cached_time = 26280000

load_dotenv('.env')

NTL_PARK_KEY = os.environ.get('NATLPARKS_KEY') #key stored in environment variable
API_URL = 'https://developer.nps.gov/api/v1/parks'

# Logger
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s %(levelname)s %(message)s', datefmt='%d-%m-%y %H:%M:%S')
log = logging.getLogger('root')


def get_response(state_input):
    # Check if park_list is in cache; otherwise, make a request on the API
    # Indentifier for National Park API is <state-input>
    cached_park_list = cache.fetch(state_input, cache_list.DataList)
    if cached_park_list:
        log.info('National Park API - Return from Cache')
        return cached_park_list
    else:
        log.info('National Park API - return from API call')
        
        try:
            query = {'stateCode': state_input, 'api_key': NTL_PARK_KEY}
            response = requests.get(API_URL, params=query)
            response.raise_for_status()  # will raise an exception for 400(client) or 500(server) errors
            data = response.json()
            park_list = get_info(data)
            #send to the cache the park list(data), identifier(state_input) and expiry
            natlParks_data_list_for_cache = cache_list.DataList(park_list, state_input, now_plus_expiry())

            cache.add(natlParks_data_list_for_cache)
            return park_list
        except requests.exceptions.HTTPError as e:
            log.exception(e)
            raise e
        except Exception as ex:
            log.exception(ex)
            raise ex


def get_info(data):
    try:
        park_list = list()
        list_of_parks = data['data']
        for park in list_of_parks:
            park_list_w_info = dict()

            if park['fullName'] and park['latitude'] and park['longitude']:
                modified_name = html.unescape(park['fullName'])
                park_list_w_info['name'] = modified_name
                park_list_w_info['lat'] = park['latitude'] 
                park_list_w_info['lon'] = park['longitude'] 
                
                if park['designation']:
                    park_list_w_info['designation'] = park['designation']
                if park['addresses']:
                    park_list_w_info['city'] = park['addresses'][0]['city']

                park_list.append(park_list_w_info)
        return park_list
    
    except Exception as e:
        log.exception(e)
        raise e


def now_plus_expiry():
    now = int(time.time())
    return now + cached_time
