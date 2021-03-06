import unittest
from unittest import TestCase

import api_calls
from api_calls import natlParks_api

class TestNatlParkAPI(TestCase):

    def test_retrieve_natlPark_info(self):
        example_api_response = {
        "data": [
        {
        "url": "https://www.nps.gov/grpo/index.htm",
        "fullName": "Grand Portage National Monument",
        "id": "E463E13F-FCD4-41B3-AEF3-BA3199E04399",
        "parkCode": "grpo",
        "latitude": "47.99294217",
        "longitude": "-89.75573031",
        "designation":"National Monument",
        "addresses": [
            {
            "postalCode": "55605",
            "city": "Grand Portage",
            "stateCode": "MN",
            }]

        } ] }
        
        #expected response = list of dictionaries
        expected_park_list = [
            {"name": "Grand Portage National Monument",
            "lat": "47.99294217",
            "lon": "-89.75573031",
            "designation": "National Monument",
            "city": "Grand Portage"}
        ]
        park_list = api_calls.natlParks_api.get_info(example_api_response)
        #compare data
        self.assertEqual(expected_park_list, park_list)
    
    
    def test_retrieve_natlPark_info_no_lat_or_lon(self):
        example_api_response = {
        "data": [
        {
        "url": "https://www.nps.gov/grpo/index.htm",
        "fullName": "Grand Portage National Monument",
        "id": "E463E13F-FCD4-41B3-AEF3-BA3199E04399",
        "parkCode": "grpo",
        "latitude": "",
        "longitude": "",
        "designation":"National Monument",
        "addresses": [
            {
            "postalCode": "55605",
            "city": "Grand Portage",
            "stateCode": "MN",
            }]

        } ] }
         #if there is no lat or lon, the park will not go on the park list
         #because we cannot access trails with no lat and lon
        expected_park_list = []
        park_list = api_calls.natlParks_api.get_info(example_api_response)
        #compare data
        self.assertEqual(expected_park_list, park_list)
    



