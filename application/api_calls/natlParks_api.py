import os
import requests
import logging
from dotenv import load_dotenv

load_dotenv('application/.env')

NTL_PARK_KEY = os.environ.get('NATLPARKS_KEY')
API_URL = 'https://developer.nps.gov/api/v1/parks'

# Logger
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s %(levelname)s %(message)s', datefmt='%d-%m-%y %H:%M:%S')
log = logging.getLogger('root')


def get_response(state):
    try:
        query = {'stateCode': state, 'api_key': NTL_PARK_KEY}
        response = requests.get(API_URL, params=query)
        response.raise_for_status()  # will raise an exception for 400(client) or 500(server) errors
        data = response.json()
        park_list = get_info(data)

        return park_list
    except Exception as ex:
        log.exception(ex)
        raise ex


def get_info(data):
    try:

        park_list = list()
        list_of_parks = data['data']
        for park in list_of_parks:
            park_list_w_info = dict()

            if len(park['fullName']) != 0:
                park_list_w_info['name'] = park['fullName']

            if len(park['latitude']) != 0:
                park_list_w_info['lat'] = park['latitude']

            if len(park['longitude']) != 0:
                park_list_w_info['lon'] = park['longitude']

            if len(park['designation']) != 0:
                park_list_w_info['designation'] = park['designation']


            if len(park['addresses']) != 0:
                park_list_w_info['city'] = park['addresses'][0]['city']
                park_list_w_info['state_code'] = park['addresses'][0]['stateCode']

            park_list.append(park_list_w_info)
        return park_list

    except Exception as e:
        log.exception(e)
        raise e
