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

    # def test_main_page(self):
    #     response = self.app.get(APP_URL, follow_redirects=True)
    #     self.assertEqual(response.status_code, 200)

    # # mock the api call and provide a list of response that will be return
    # @patch('app.natlParks_api.get_response')
    # def test_state_page(self, get_response):
    #     get_response.return_value = [{'name': 'Canyon de Chelly National Monument', 'lat': '36.14319567',
    #                                                          'lon': '-109.3388303', 'designation': 'National Monument', 'city': 'Chinle'},
    #                                                         {'name': 'Casa Grande Ruins National Monument', 'lat': '32.99702582',
    #                                                          'lon': '-111.5325383', 'designation': 'National Monument', 'city': 'Coolidge'}]
    #     url = APP_URL+'parks?states=AZ'
    #     # assert list of parks on page
    #     # make request
    #     response = self.app.get(url)
    #     self.assertIn(b'Canyon de Chelly National Monument', response.data)

    # # mock api call to the trail and weather api
    # @patch('app.hiking_api.get_trails',return_value = [{'name': 'National Parks Marathon Project - Voyageurs National Park', 'length': 25.4, 'difficulty': 'blue', 'summary': 'An amazing green experience running in dense forest.'}, {'name': 'Locator Lake Trail', 'length': 2, 'difficulty': 'blue', 'summary': 'This trail is awesome!'}])
    # @patch('app.weather_api.get_weather',return_value = [{'date': '2020-10-29', 'temp': {'day': 25.3, 'min': 17.67, 'max': 26.83, 'night': 21.78, 'eve': 22.89, 'morn': 17.67}, 'desc': 'Overcast Clouds', 'humidity': 58}, {'date': '2020-10-30', 'temp': {'day': 33.91, 'min': 20.82, 'max': 35.85, 'night': 30.96, 'eve': 32.92, 'morn': 20.82}, 'desc': 'Broken Clouds', 'humidity': 89}])
    # def test_get_info_for_park(self, get_hiking, get_weather):
    #     url = APP_URL + '/moreinfo/MN/Voyageurs%20National%20Park/48.48370609/-92.8382913'

    #     response = self.app.get(url)
    #     self.assertIn(b'National Parks Marathon Project - Voyageurs National Park', response.data)
    #     self.assertIn(b'Overcast Clouds', response.data)
    #     self.assertIn(b'blue', response.data)
    
    # def test_save_trail(self):
    #     url = APP_URL + '/moreinfo/AL/Little%20River%20Canyon%20National%20Preserve/34.41461863/-85.61734327'
    #     response = self.app.post(url, data={'trail-obj': " {'name': 'Cruiser Lake Trail', 'length': 10.9, 'difficulty': 'greenBlue', 'summary': 'N/A'} "},follow_redirects=True)
        
    #     self.assertIn(b'Cruiser Lake Trail', response.data)
    #     self.assertIn(b'AL', response.data)
    #     self.assertIn(b'Little River Canyon National Preserve', response.data)
        
    

    

    def test_save_trail_already_saved(self):
        # http://localhost:5000/moreinfo/UT/Zion%20National%20Park/37.29839254/-113.0265138
        trail_01 = {'trail-obj': " {'name': 'Angels Landing', 'length': 4.4, 'difficulty': 'black', 'summary': 'One of the most memorable National Park hikes. Heavenly views await at the end of an exposed ridge.'} "}
        trail_02 = {'trail-obj': " {'name': 'Canyon Overlook Trail', 'length': 0.7, 'difficulty': 'blue', 'summary': 'A short trail that leads to incredible views of Zion Canyon.'} "}
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

        # Add trail_01 again, which might try an error here
        url = APP_URL + '/moreinfo/UT/Zion%20National%20Park/37.29839254/-113.0265138'
        
        response_03 = self.app.post(url, data= trail_01, follow_redirects=True)
        # Will be redirected to the abort(400) page and have a message saying the trail already exist in the database
        self.assertIn(b'Angels Landing is already in the database. Please try to save another trail to the system', response_03.data)
        

        
    # def test_state_page_bad_params(self):
    #     # Should we be checking it on flask app instead ?if so what exception should be thrown? 
    #     # you should not throw exceptions from the flask routes. The back end methods may throw exceptions to represent an error condition
    #     # and your flask route handler would have try-except for that 
    #     # Always return a HTTP response, even if it's a 500 response. 
    #     url = APP_URL+'parks?states=empty'
    #     # make the request
    #     # your server should return a 400 bad request or a 404 not found for this request.  So make the request and assert the status code 
    #     # is as expected. 
    #     self.fail()

    # # TODO test for bad url or non-existent api call like state that does not exist etc...
    # # test these URLs, the test would be very similar to the one above
    # #         url = APP_URL+'parks?somethingelse=whatever'  
    # #         url = APP_URL+'parks'  

    # def test_invalid_state_in_state_page(self):
    #     self.fail()

    # def test_invalid_lat_lon_on_api_call(self):
    #     # !QUESTION: Not sure where to catch the exception where the lat and long is empty like this `http://localhost:5000/moreinfo/AL/Freedom%20Riders%20National%20Monument//` only able to catch the exception when the lat and lon is random number
    #     # !QUESTION: Should I be using the self.app.get(url) and mock the abort page here too?
    #     # you don't need to mock the abort page. Again make the request and check you get a response with the appropriate status code
    #     # the flask app route needs to be checking the parameters and returning 400 or 404 if they don't make sense
    #     self.fail()

    # def test_api_call_is_down(self):
    #     # !QUESTION: for this one will this be the abort(500) page? or we will need to add an additional exception in the flask app?
    #     # mock the api call(s) to return error or raise exception, whatever they do if the server is down
    #     # make a call
    #     # assert 500 error code with the message you set. 
    #     self.fail()


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
