from peewee import *
from models import Trails

### use these functions to preform actions in the database

def add_saved_trail(name, leng, dif, summ, natl_pk, state):
    
    Trails.create(trail_id = AutoField, trail_name = name, trail_len = leng, trail_difficulty = dif , trail_sum = summ, natl_park = natl_pk, date_saved = DateTimeField, state = state)
    print(f'{name} has been added')


def delete_trail_by_id(trail_id):

    query = Trails.delete().where(Trails.trail_id == trail_id)
    query.execute()

def delete_everything():
    """ Deletes all trails from database"""
    Trails.delete().execute()


def get_all_saved_trails():
    """ Returns everything in db"""
    query = Trails.select()
    return list(query)

def get_id_by_trail_name(name):

    trail_id = Trails.get_id().where(Trails.trail_name == name)
    return trail_id


def saved_trail_count():
    """ :returns the number of saved trails in the db """
    return Trails.select().count()