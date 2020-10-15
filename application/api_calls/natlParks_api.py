import os
import requests
import logging
from dotenv import load_dotenv
from .state_name_and_code import us_state_abbrev

from . import state_name_and_code as state_obj

load_dotenv('application/.env')

NTL_PARK_KEY = os.environ.get('NATLPARKS_KEY')
print(NTL_PARK_KEY)
API_URL = 'https://developer.nps.gov/api/v1/parks'

# Logger
logging.basicConfig(filename='debug.log', level=logging.DEBUG,
                    format=f'%(asctime)s - %(name)s - %(levelname)s - %(message)s ')

state_code = us_state_abbrev.values()
state_name = us_state_abbrev.keys()


def get_all_state_name():
    state_list = us_state_abbrev.values()

    return state_list


def get_response(state):
    try:
        query = {'stateCode': state, 'api_key': NTL_PARK_KEY}
        response = requests.get(API_URL, params=query)
        response.raise_for_status()  # will raise an exception for 400(client) or 500(server) errors
        data = response.json()
        park_list = get_info(data)

        return park_list
    except Exception as ex:
        logging.exception(ex)
        return ex


def get_info(data):
    park_list = list()
    list_of_parks = data['data']
    for park in list_of_parks:
        parkName = park['fullName']
        lat = park['latitude']
        longitude = park['longitude']
        designation = park['designation']
        city = park['addresses'][0]['city']
        stateCode = park['addresses'][0]['stateCode']
        print(parkName)
        print(park_list)
        park_list.append(parkName)

    return park_list
    # print(
    #     f'{parkName}, located in {city}, {stateCode}, is a {designation}.')  # '; a few activities {list_of_act[0:5]} Image caption: {image_caption} Location: latitude {lat} and longitude{longitude}  \n')
