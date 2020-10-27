import os
from unittest import TestCase
from ..database import db_config
from peewee import SqliteDatabase

db_config.database_path = 'test_hiking_trails.db'

# TODO: Do I need this?
# TEST_DB = SqliteDatabase(TEST_DB_PATH)
from ..database import models,database_functions
from application import app


# https://www.patricksoftwareblog.com/unit-testing-a-flask-application/
class BasicTests(TestCase):


    # executed prior to each test
    def setUp(self):
        app.config['TESTING'] = True
        app.config['DEBUG'] = False
        # app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + \
        #                                         os.path.join(app.config['BASEDIR'], TEST_DB)
        # app.config[]
        # TODO: Should I include the Config file for DB?
        # Create a new DB
        # TODO: Should I use the function to start a new DB instead?
        # self.hiking_trails_db = models.initialize_db()

        # Clear all tables in DB
        # TODO: is this correct
        models.Trails.delete().execute()

        self.app = app.test_client()

        self.assertEqual(app.debug, False)

    # executed after each test
    def tearDown(self):
        pass

    ###############
    #### tests ####
    ###############

    def test_main_page(self):
        response = self.app.get('/', follow_redirects=True)
        self.assertEqual(response.status_code, 200)


if __name__ == "__main__":
    unittest.main()
