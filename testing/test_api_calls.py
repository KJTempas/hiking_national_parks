import unittest
from unittest import TestCase
from unittest.mock import patch

import api_calls

class TestNatlParkAPI(TestCase):

    @patch('requests.get')
    def test_api_response(self, mock_request_get):
        mock_park_name = "Grand Portage National Monument"
        example_api_response = { 
            "data": [
            {
            "fullName": mock_park_name,
            "latitude": "47.99294217",
            "longitude": "-89.75573031",
            "states": "MN",
            "images": [],
            "name": "Grand Portage",
            "designation": "National Monument"
            }]   }    
        
        #mock for the mock_requests_get
        mock_request_get().json.return_value= example_api_response
        park = example_api_response[0]
        parkName = natlParks_api.get_info(example_api_response.parkName = park['fullName']  )




