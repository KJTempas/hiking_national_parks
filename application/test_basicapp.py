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
    @patch('app.hiking_api.get_trails')
    @patch('app.weather_api.get_weather')
    def test_get_info_for_park(self, get_hiking, get_weather):
        # TODO here!
        url = LOCAL_HOST_URL + '/moreinfo/MN/Voyageurs%20National%20Park/48.48370609/-92.8382913'
        # 'http://localhost:5000/moreinfo/MN/Voyageurs%20National%20Park/48.48370609/-92.8382913'
        get_hiking.return_value = [{'name': 'National Parks Marathon Project - Voyageurs National Park', 'length': 25.4, 'difficulty': 'blue', 'summary': 'An amazing green experience running in dense forest.'}, {'name': 'Locator Lake Trail', 'length': 2, 'difficulty': 'blue', 'summary': 'This trail is awesome!'}]
        get_weather.return_value = [{'date': '2020-10-29', 'temp': {'day': 25.3, 'min': 17.67, 'max': 26.83, 'night': 21.78, 'eve': 22.89, 'morn': 17.67}, 'desc': 'Overcast Clouds', 'humidity': 58}, {'date': '2020-10-30', 'temp': {'day': 33.91, 'min': 20.82, 'max': 35.85, 'night': 30.96, 'eve': 32.92, 'morn': 20.82}, 'desc': 'Broken Clouds', 'humidity': 89}]

        response = self.app.get(url)
        self.assertIn(b'National Parks Marathon Project - Voyageurs National Park', response.data)
        # self.aasertIn(b'Overcast Clouds', response.data)
        # self.assertNotIn(b'blue', response.data)

        # self.fail()

    #
    # def test_save_trail(self):
    #     self.fail()
    #
    # def test_save_trail_already_saved(self):
    #     self.fail()
    #
    # def test_state_page_bad_params(self):
    #     self.fail()

    # TODO test for bad url or non-existent api call like state that does not exist etc...
    ###########
    # Example #
    ###########
    # # Ensure that welcome page loads
    # def test_welcome_route_works_as_expected(self):
    #     response = self.client.get('/welcome', follow_redirects=True)
    #     self.assertIn(b'Welcome to Flask!', response.data)
    #
    # # Ensure that posts show up on the main page
    # def test_posts_show_up_on_main_page(self):
    #     response = self.client.post(
    #         '/login',
    #         data=dict(username="admin", password="admin"),
    #         follow_redirects=True
    #     )
    #     self.assertIn(b'This is a test. Only a test.', response.data)

if __name__ == "__main__":
    unittest.main()
