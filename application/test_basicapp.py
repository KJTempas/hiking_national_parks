import os
import unittest
from unittest.mock import patch

from database import db_config
from peewee import SqliteDatabase

db_config.database_path = 'test_hiking_trails.db'

from database import models, database_functions
from app import *

LOCAL_HOST_URL = 'http://127.0.0.1:5000/'

# https://www.patricksoftwareblog.com/unit-testing-a-flask-application/
class BasicTests(unittest.TestCase):


    # executed prior to each test
    def setUp(self):
        app.config['TESTING'] = True
        app.config['DEBUG'] = False
        # Create a new DB
        self.hiking_trails_db = models.initialize_db()
        # Clear all tables in DB
        models.Trails.delete().execute()

        self.app = app.test_client()
        self.assertEqual(app.debug, False)

    # executed after each test
    def tearDown(self):
        pass

    def test_main_page(self):
        response = self.app.get(LOCAL_HOST_URL, follow_redirects=True)
        self.assertEqual(response.status_code, 200)

    # mock the api call and provide a list of response that will be return
    @patch('app.natlParks_api.get_response')
    def test_state_page(self, get_response):
        get_response.return_value = [{'name': 'Canyon de Chelly National Monument', 'lat': '36.14319567',
                                                             'lon': '-109.3388303', 'designation': 'National Monument', 'city': 'Chinle'},
                                                            {'name': 'Casa Grande Ruins National Monument', 'lat': '32.99702582',
                                                             'lon': '-111.5325383', 'designation': 'National Monument', 'city': 'Coolidge'}]
        url = LOCAL_HOST_URL+'parks?states=AZ'
        # assert list of parks on page
        # make request
        response = self.app.get(url)
        self.assertIn(b'Canyon de Chelly National Monument', response.data)

    # mock api call to the trail and weather api
    @patch('app.hiking_api.get_trails',return_value = [{'name': 'National Parks Marathon Project - Voyageurs National Park', 'length': 25.4, 'difficulty': 'blue', 'summary': 'An amazing green experience running in dense forest.'}, {'name': 'Locator Lake Trail', 'length': 2, 'difficulty': 'blue', 'summary': 'This trail is awesome!'}])
    @patch('app.weather_api.get_weather',return_value = [{'date': '2020-10-29', 'temp': {'day': 25.3, 'min': 17.67, 'max': 26.83, 'night': 21.78, 'eve': 22.89, 'morn': 17.67}, 'desc': 'Overcast Clouds', 'humidity': 58}, {'date': '2020-10-30', 'temp': {'day': 33.91, 'min': 20.82, 'max': 35.85, 'night': 30.96, 'eve': 32.92, 'morn': 20.82}, 'desc': 'Broken Clouds', 'humidity': 89}])
    def test_get_info_for_park(self, get_hiking, get_weather):
        url = LOCAL_HOST_URL + '/moreinfo/MN/Voyageurs%20National%20Park/48.48370609/-92.8382913'

        response = self.app.get(url)
        self.assertIn(b'National Parks Marathon Project - Voyageurs National Park', response.data)
        self.assertIn(b'Overcast Clouds', response.data)
        self.assertIn(b'blue', response.data)

    @patch('database.database_functions.add_trail')
    def test_save_trail(self, mock_add_trail):
        url = LOCAL_HOST_URL + '/moreinfo/MN/Voyageurs%20National%20Park/48.48370609/-92.8382913'
        response = self.app.post(url)
        log.info(response)
        self.fail()
    
    # TODO: this function should be redirect to the error page
    @patch('database_functions.add_trail')
    @patch('code.abort')
    def test_save_trail_already_saved(self, add_trail, mock_abort):
        # TODO add some data with add_trails function?
        # then assert called_once_with
        self.fail()

    def test_state_page_bad_params(self):
        self.fail()

    # TODO test for bad url or non-existent api call like state that does not exist etc...

    def test_invalid_state_in_state_page(self):
        self.fail()

    def test_invalid_lat_lon_on_api_call(self):
        self.fail()

    def test_api_call_is_down(self):
        self.fail()


if __name__ == "__main__":
    unittest.main()



#
# # code.py
#
# from flask import abort
#
#
# def my_function():
#     abort(400, "error")

# # test.py
#
# import unittest
# from unittest.mock import patch
# from werkzeug import exceptions
#
# import code  # Your code file code.py
#
#
# class Tests(unittest.TestCase):
#
#     @patch('code.abort')
#     def test_one(self, mock_abort):
#         code.my_function()
#         mock_abort.assert_called_once_with(400, 'error')
#
#     def test_two(self):
#         with self.assertRaises(exceptions.BadRequest):
#             code.my_function()
#
#     def test_three(self):
#         with self.assertRaisesRegexp(exceptions.BadRequest, '400 Bad Request: error'):
#             code.my_function()
#
#
# unittest.main(argv=[''], verbosity=2, exit=False)