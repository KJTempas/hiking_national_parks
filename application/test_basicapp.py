import os
import unittest
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




if __name__ == "__main__":
    unittest.main()
