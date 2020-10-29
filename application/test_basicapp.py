import os
import unittest
from unittest.mock import patch

from database import db_config
from peewee import SqliteDatabase

db_config.database_path = 'test_hiking_trails.db'

from database import models, database_functions
from app import *


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
        response = self.app.get('/', follow_redirects=True)
        self.assertEqual(response.status_code, 200)

    # mock the api call and provide a list of response that will be return
    # TODO should change the return_value into something similar to the request response
    @patch('app.natlParks_api.get_response', return_value=['Sequoia', 'Mojave'])
    def test_state_page(self, get_response):
        url = 'http://127.0.0.1:5000/parks?state=CA'
        # assert list of parks on page
        # make request
        response = self.app.get(url)
        print(response.data)
        self.assertIn('Sequoia', get_response)


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
