import unittest
from unittest import TestCase

# import sys, os

# sys.path.append(os.path.abspath(os.path.join('..', db_config)))

import db_config

db_config.database_path = 'test_hiking_trails.db'

import database_functions
from models import Trails

class TestTrails(TestCase):


    def clear_db(self):
        database_functions.delete_everything()


    def add_test_data(self):
        ### Adds 3 pieces of db data
        self.trl1 = Trails(trail_name = 'trail1', trail_len = 2, trail_difficulty = 'blue' , trail_sum = 'summary', natl_park = 'Yosemite', state = 'MT')
        self.trl2 = Trails(trail_name = 'trail2', trail_len = 5, trail_difficulty = 'black' , trail_sum = 'summary2', natl_park = 'Lake Itasca', state = 'MN')
        self.trl3 = Trails(trail_name = 'trail3', trail_len = 6, trail_difficulty = 'green' , trail_sum = 'summary3', natl_park = 'Grand Canyon', state = 'CO')

        self.trl1.save()
        self.trl2.save()
        self.trl3.save()



    def test_add_trail_empty_db(self):
        self.clear_db()
        self.trl1 = Trails( trail_name = 'trail1', trail_len = 2, trail_difficulty = 'blue' , trail_sum = 'summary', natl_park = 'Yosemite', state = 'MT')
        self.trl1.save()
        self.assertEqual(1, database_functions.saved_trail_count())

if __name__ == '__main__':
    unittest.main()



