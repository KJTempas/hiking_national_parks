import os
import requests
import logging
from dotenv import load_dotenv

load_dotenv('application/.env')

key = os.environ.get('NATLPARKS_KEY')
url = 'https://developer.nps.gov/api/v1/parks'
logging.basicConfig(filename='debug.log', level=logging.DEBUG,
                    format=f'%(asctime)s - %(name)s - %(levelname)s - %(message)s ')

state_codes = ['AL', 'AK', 'AZ', 'AR', 'CA', 'CO', 'CT', 'DE', 'DC', 'FL', 'GA', 'HI', 'ID', 'IL', 'IN', 'IA', 'KS',
               'KY', 'LA', 'ME', 'MD', 'MA', 'MI', 'MN', 'MS', 'MO', 'MT', 'NE',
               'NV', 'NH', 'NJ', 'NM', 'NY', 'NC', 'ND', 'OH', 'OK', 'OR', 'PA', 'RI', 'SC', 'SD', 'TN', 'TX', 'UT',
               'VT', 'VA', 'WA', 'WV', 'WI', 'WY']


def main():
    state = get_state()
    data = get_response(state)
    get_info(data)


def get_state():
    while True:
        try:
            state = input('Enter a two-letter state code  ')
            if state.upper() in state_codes:
                return state.upper()
            else:
                print('Please enter a valid state code')
        except ValueError:
            print('Please enter a 2 letter state code')


def get_response(state):
    try:
        query = {'stateCode': state, 'api_key': key}
        response = requests.get(url, params=query)
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
        park_list.append(parkName)

    return park_list
        # print(
        #     f'{parkName}, located in {city}, {stateCode}, is a {designation}.')  # '; a few activities {list_of_act[0:5]} Image caption: {image_caption} Location: latitude {lat} and longitude{longitude}  \n')


if __name__ == '__main__':
    main()
