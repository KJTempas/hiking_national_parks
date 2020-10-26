import os #needed?
import tempfile #needed?
#import pytest

import unittest
from unittest import TestCase

import app

#from database import models #maybe needed for further testing
#from models import Trails #when do you need . before models?


class TestHomePage(TestCase):
    def test_home_page_shows_headers(self):
        #home_page_url = '/'
        response = self.client.get('') #home page url - go to home page
        self.assertTemplateUsed(response, 'templates/index.html')
        #these are not really responses, but should appear on home page
        self.assertContains(response, "National Park and Trail Manager") 
        #self.assertContains(response, "Please select the state that you want to visit" )
        self.assertContains(response, "Please select the state that you want to go" )
        

class TestShowParksPage(TestCase):
    def test_natl_parks_page(self):
        response = self.client.get('/parks')
        self.assertTemplateUsed(response, 'templates/park_list.html')
        

class TestShowHikingAndWeatherPage(TestCase):
    def test_hiking_and_weather_page(self):
        response = self.client.get('/moreinfo/<state>/<park>/<lat>/<lon>')
        self.assertTemplateUsed(response, 'templates/hikes_weather.html')

#TODO make fixtures file with some national park names, etc
#TODO ? make a separate fixtures file withe some hiking trail and weather data?





#this client fixture is called by each test

    #below from flask.palletsproject.com/en/1.1.x/testing
# @pytest.fixture
# def client():
#   db_fd, application.app.config['DATABASE'] = tempfile.mkstemp()
#   flaskr.app.config['TESTING'] = True\
#   with flaskr.app.test_client() as client:
#       with flaskr.app.app_context():
#           flaskr.init_db()
#       yield client
#   os.close(db_fd)
#   os.unlink(flaskr.app.config['DATABASE'])


# @pytest.fixture
# def client():
#   db_fd, flaskr.app.config['DATABASE'] = tempfile.mkstemp()
#   flaskr.app.config['TESTING'] = True\
#   with flaskr.app.test_client() as client:
#       with flaskr.app.app_context():
#           flaskr.init_db()
#       yield client
#   os.close(db_fd)
#   os.unlink(flaskr.app.config['DATABASE'])

#https://www.patricksoftwareblog.com/testing-a-flask-application-using-pytest/
# @pytest.fixture
# def client(scope='module'):
#     flask_app = create_app('flask_test.cfg')
#     testing_client = flask_app.test_client()

#     #establish an application context before running tests
#     ctx = flask_app.app_context()
#     ctx.push()
#     yield testing_client #where the testing happens
#     ctx.pop()

#database should start out empty as no bookmarks saved yet
# def test_empty_db(client):
#     rv = client.get('/')
#     assert b'No entries here so far' in rv.data


# def test_home_page(self):
#     response = client.get('/')
#     assert response.status_code==200
#     assert b"National Park and Trail Manager" in response.data
#     assert b"Please select the state that you want to visit" in response.data

# def test_home_page_alt_version(self):
#     response = client.get('/')
#     assert response.status_code==200
#     self.assertContains(response, "National Park and Trail Manager") 
#     self.assertContains(response, "Please select the state that you want to visit" )



#in a separate file for functional tests?
# class TitleTest(LiveServerTestCase):
#   @classmethod
#   def setUpClass(cls):
#     super().setUpClass()
#     cls.selenium == WebDriver()
#     cls.selenium.implicitly_wait(10)

#   @classmethod
#   def tearDownClass(cls):
#     cls.selenium.quit()
#     super.tearDownClass()

#   def test_title_in_browser_on_home_page(self):
#     self.selenium.get(self.live_server_url)
#     self.assertIn('    ', self.selenium.title)

