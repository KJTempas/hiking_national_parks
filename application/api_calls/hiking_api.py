import requests
import os
from dotenv import load_dotenv

load_dotenv('application/.env')

HIKING_KEY = os.environ.get('HIKING_KEY')


HIKING_URL = 'https://www.hikingproject.com/data/get-trails'


def get_trails(lat, lon):

    query = {'lat': lat, 'lon': lon, 'key': HIKING_KEY}

    data = requests.get(HIKING_URL, params=query).json()
    trail_list = list()
    ##example  print for 5 results
    for x in range(-1, 5):
        trail_name = data['trails'][x]['name']
        trail_summary = data['trails'][x]['summary']
        trail_length = data['trails'][x]['length']
        trail_difficulty = data['trails'][x]['difficulty']
        trail_img = data['trails'][x]['imgMedium']
        trail_list.append(trail_name)
        #
        # print(
        #     f'Name: {trail_name} | Trail summary: {trail_summary} | Trail length: {trail_length} | Trail difficulty: {trail_difficulty} | Trail img: {trail_img}')
    return trail_list