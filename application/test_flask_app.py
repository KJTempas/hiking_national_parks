import os
import unittest
from unittest.mock import patch

from database import db_config
from peewee import SqliteDatabase

db_config.database_path = 'test_trails.db'

from database import models, database_functions
import database
from database.models import Trails
from app import *

APP_URL = 'http://127.0.0.1:5000/'

# https://www.patricksoftwareblog.com/unit-testing-a-flask-application/
class BasicTests(unittest.TestCase):

    # executed prior to each test
    def setUp(self):
        app.config['TESTING'] = True
        app.config['DEBUG'] = False
        # Create a new DB
        self.hiking_trails_db = database.models.initialize_db()
        # Clear all tables in DB
        Trails.delete().execute()

        self.app = app.test_client()
        self.assertEqual(app.debug, False)
        
    # executed after each test
    def tearDown(self):
        pass

    def test_main_page(self):
        # To ensure the main page is running as expected
        response = self.app.get(APP_URL, follow_redirects=True)
        self.assertEqual(response.status_code, 200)

    # mock the national park api call and provide a list of response that will be return
    @patch('app.natlParks_api.get_response')
    def test_state_page(self, get_response):
        # The expected return value for the mock national park api call function 
        get_response.return_value = [{'name': 'Canyon de Chelly National Monument', 'lat': '36.14319567',
                                                             'lon': '-109.3388303', 'designation': 'National Monument', 'city': 'Chinle'},
                                                            {'name': 'Casa Grande Ruins National Monument', 'lat': '32.99702582',
                                                             'lon': '-111.5325383', 'designation': 'National Monument', 'city': 'Coolidge'}]
        
        # The request url
        url = APP_URL+'parks?states=AZ'
        
        # To make request
        response = self.app.get(url)

        # Make sure the national park is being show on the national park page (the localhost:500/parks route)
        self.assertIn(b'Canyon de Chelly National Monument', response.data)

    # mock hiking and weather api call 
    # which will return some sample data 
    @patch('app.hiking_api.get_trails',return_value = [{'name': 'National Parks Marathon Project - Voyageurs National Park', 'length': 25.4, 'summary': 'An amazing green experience running in dense forest.'}, {'name': 'Locator Lake Trail', 'length': 2, 'summary': 'This trail is awesome!'}])
    @patch('app.weather_api.get_weather',return_value = [{'date': '2020-10-29', 'temp': {'day': 25.3, 'min': 17.67, 'max': 26.83, 'night': 21.78, 'eve': 22.89, 'morn': 17.67}, 'desc': 'Overcast Clouds', 'humidity': 58}, {'date': '2020-10-30', 'temp': {'day': 33.91, 'min': 20.82, 'max': 35.85, 'night': 30.96, 'eve': 32.92, 'morn': 20.82}, 'desc': 'Broken Clouds', 'humidity': 89}])
    def test_get_info_for_park(self, get_hiking, get_weather):
        
        # The trails and weather route/url
        url = APP_URL + '/moreinfo/MN/Voyageurs%20National%20Park/48.48370609/-92.8382913'

        # Make request
        response = self.app.get(url)

        # Check if the expected value is in the page or the response
        self.assertIn(b'National Parks Marathon Project - Voyageurs National Park', response.data)
        self.assertIn(b'Overcast Clouds', response.data)
    
    def test_save_trail(self):
        # Route/URL to save trails
        url = APP_URL + '/moreinfo/AL/Little%20River%20Canyon%20National%20Preserve/34.41461863/-85.61734327'

        # Make request
        response = self.app.post(url, data={'trail-obj': " {'name': 'Cruiser Lake Trail', 'length': 10.9, 'summary': 'N/A'} "},follow_redirects=True)
        
        # Check if the expected value is in the page or the response
        self.assertIn(b'Cruiser Lake Trail', response.data)
        self.assertIn(b'AL', response.data)
        self.assertIn(b'Little River Canyon National Preserve', response.data)
        
    
    def test_save_trail_already_saved(self):
        # Some sample trail object to test saving into the database
        trail_01 = {'trail-obj': " {'name': 'Angels Landing', 'length': 4.4, 'summary': 'One of the most memorable National Park hikes. Heavenly views await at the end of an exposed ridge.'} "}
        trail_02 = {'trail-obj': " {'name': 'Canyon Overlook Trail', 'length': 0.7, 'summary': 'A short trail that leads to incredible views of Zion Canyon.'} "}
        
        # Add some trail_01
        url = APP_URL + '/moreinfo/UT/Zion%20National%20Park/37.29839254/-113.0265138'
        response = self.app.post(url, data= trail_01, follow_redirects=True)
        
        # Check if the `trail_01` has been added to the database
        self.assertIn(b'Angels Landing', response.data)

        # Add trail_02
        url = APP_URL + '/moreinfo/UT/Zion%20National%20Park/37.29839254/-113.0265138'
        response_02 = self.app.post(url, data= trail_02, follow_redirects=True)
        # Check if the `trail_02` has been added to the database
        self.assertIn(b'Canyon Overlook Trail', response_02.data)

        # Add trail_01 again, which might throw an exception and redirected to the error page with some message for the user
        url = APP_URL + '/moreinfo/UT/Zion%20National%20Park/37.29839254/-113.0265138'
        
        response_03 = self.app.post(url, data= trail_01, follow_redirects=True)
        # Will be redirected to the abort(400) page and have a message saying the trail already exist in the database
        self.assertIn(b'Angels Landing is already in the database. Please try to save another trail to the system', response_03.data)
        
        
    def test_state_page_bad_params_or_non_existent_api_call(self):

        # Test when there is an invalid states code being provided
        url_01 = APP_URL+'parks?states=empty'
        response_01 = self.app.get(url_01)

        # Test when there is no input being provided for the states code
        url_02 = APP_URL+'parks?states='
        response_02 = self.app.get(url_02)

        # Test when the states parameter has invalid value
        url_03 = APP_URL+'parks?states=1221'
        response_03 = self.app.get(url_03)

        # Test when the route consists of non-existent api-call
        url_04 = APP_URL+'parks?random=statenamehere'
        response_04 = self.app.get(url_04)

        # Test when the route has no parameters provided
        url_05 = APP_URL+'parks'
        response_05 = self.app.get(url_05)

        # Expected message that will be showing to the user when an exception is being thrown
        self.assertIn(b'The URL is invalid. Please double check your spelling', response_01.data)
        self.assertIn(b'The URL is invalid. Please double check your spelling', response_02.data)
        self.assertIn(b'The URL is invalid. Please double check your spelling', response_03.data)
        self.assertIn(b'The URL is invalid. Please double check your spelling', response_04.data)
        self.assertIn(b'The URL is invalid. Please double check your spelling', response_05.data)

   
    def test_get_trail_and_weather_page_with_bad_params(self):

        # Test `/moreinfo/<state>/<national_park>/lat/lon` route
        # When this route has a bad params, 
        # the expected behavior to be redirected to the error.html page 
        # with an error message on the page in order to let the user know the route is wrong.
        
        # This is an Error 404
        url_01 = APP_URL + '/moreinfo/UT/Zion%20National%20Park//'
        response_01 = self.app.get(url_01)
        self.assertIn(b'The URL is invalid. Please double check your spelling', response_01.data)
        
        # This is an Error 403 
        url_02 = APP_URL + '/moreinfo/UT/Zion%20National%20Park/asd/qweqw'
        response_02 = self.app.get(url_02)
        self.assertIn(b'The page you are looking for is not available. Please try again later.', response_02.data)
        
        # This is an Error 404
        url_03 = APP_URL + '/moreinfo//Zion%20National%20Park/37.29839254/-113.0265138'
        response_03 = self.app.get(url_03)
        self.assertIn(b'The URL is invalid. Please double check your spelling', response_03.data)
        
        # This is an Error 404
        url_04 = APP_URL + '/moreinfo/UT//37.29839254/-113.0265138'
        response_04 = self.app.get(url_04)
        self.assertIn(b'The URL is invalid. Please double check your spelling', response_04.data)
        
        # This is an Error 400
        url_05 = APP_URL + '/moreinfo/UT/123123/37.29839254/-113.0265138'
        response_05 = self.app.get(url_05)
        self.assertIn(b'The URL is invalid. Please double check your spelling', response_05.data)

        # This is an Error 400
        url_06 = APP_URL + '/moreinfo/49/Test National Park/37.29839254/-113.0265138'
        response_06 = self.app.get(url_06)
        self.assertIn(b'The URL is invalid. Please double check your spelling', response_06.data)
    
    @patch('app.natlParks_api.NTL_PARK_KEY', return_value='')
    @patch('app.hiking_api.HIKING_KEY', return_value='')
    @patch('app.weather_api.WEATHER_KEY', return_value='')
    def test_api_call_is_down(self, mock_national_park_api_key,mock_hiking_api_key, mock_weather_api_key):
        # Test when missing api_key for national park api call 
        # To mock when the API call is down
        url_01 = APP_URL+'parks?states=AZ'
        response_01 = self.app.get(url_01)
        self.assertIn(b'The page you are looking for is not available. Please try again later.', response_01.data)
        # Test when missing api_key for hiking and weather api call 
        # To mock when the API call is down
        url_02 = APP_URL + '/moreinfo/UT/Zion%20National%20Park/37.29839254/-113.0265138'
        response_02 = self.app.get(url_02)
        self.assertIn(b'The page you are looking for is not available. Please try again later.', response_02.data)

if __name__ == "__main__":
    unittest.main()

