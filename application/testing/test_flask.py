import os #needed?
import tempfile #needed?
#import pytest

import unittest
from unittest import TestCase

from flask import Flask
from flask_testing import TestCase
from flask.testing import FlaskClient #palletsproject.com

import app #what I'm going to test

#from database import models #maybe needed for further testing
#from models import Trails #when do you need . before models?
#https://pythonhosted.org/Flask-Testing/


class MyTest(TestCase): #from pythonhosted.org/Flask-Testing/
    def create_app(self):
        app = Flask(__name__)
        app.config['TESTING'] = True 
        return app

#app.testing = True
#client = app.test_client()

class CustomClient(FlaskClient):
    def __init__(self, *args, **kwargs):
        self.authentication= kwargs.pop("authentication")
        super(CustomClient,self).__init__( *args, **kwargs)
app.test_client_class = CustomClient
client = app.test_client(authentication='Basic ....')

    #test_client_class = None

flask.url_for(park_list.html)

#another way to set up client/app? frm The testing skeleton section
# @pytest.fixture#but this uses pytest, not unittest
# def client():
#   db_fd, application.app.config['DATABASE'] = tempfile.mkstemp()
#   application.app.config['TESTING'] = True
#   with application.app.test_client() as client:
#       with flaskr.app.app_context():
#           flaskr.init_db()
#       yield client
#   os.close(db_fd)
#   os.unlink(flaskr.app.config['DATABASE'])


    #testing JSON responses
# @app.route('/parks')
# def some_json():
#     return jsonify(success=True)
# class TestViews(TestCase):
#     def test_some_json(self):
#         response = self.client.get('/parks')
#         self.assertEqals(response.json, dict(success=True))

#next 2 classes from Opt to not render templates in https://pythonhosted.org/Flask-Testing/
# class TestNotRenderTemplates(TestCase):
#     render_templates = False
#     def test_assert_not_process_the_template(self):
#         response = self.client.get('/parks')
#         assert '' == response.data

class TestNotRenderTemplates(TestCase): 
    render_templates = False
    def test_assert_correct_template_used_to_display_parks(self):
        response = self.client.get('/parks')
        self.assert_template_used('parklist.html')


class TestShowNatlParksList(TestCase):
    with app.test_client() as c:
        rv = c.get('/', )  #get the home page
        self.assertContains(rv, state_dict)


class TestShowNatlParks_after_choosing_state(TestCase):
    fixtures = ['test_parks']

    with app.test_client() as c: #connect to the test_client
        #rv = c.get('?state_input=mn')  #rv?
        response = c.get('/parks', 'mn') #call GET method with this url providing mn as state_input
        self.assertContains(response, 'Grand Portage National Monument')

#NOTE there is guidance - API test for response in pythonhosted.org/Flask-Testing/


# class TestHomePage(TestCase):
#     def test_home_page_shows_headers(self):
#         #home_page_url = '/'
#         response = self.client.get('') #home page url - go to home page
#         self.assertTemplateUsed(response, 'templates/index.html')
#         #these are not really responses, but should appear on home page
#         self.assertContains(response, "National Park and Trail Manager") 
#         #self.assertContains(response, "Please select the state that you want to visit" )
#         self.assertContains(response, "Please select the state that you want to go" )
        

# class TestShowParksPage(TestCase):
#     def test_natl_parks_page(self):
#         response = self.client.get('/parks')
#         self.assertTemplateUsed(response, 'templates/park_list.html')
        

# class TestShowHikingAndWeatherPage(TestCase):
#     def test_hiking_and_weather_page(self):
#         response = self.client.get('/moreinfo/<state>/<park>/<lat>/<lon>')
#         self.assertTemplateUsed(response, 'templates/hikes_weather.html')

#TODO make fixtures file with some national park names, etc
#TODO ? make a separate fixtures file withe some hiking trail and weather data?









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

