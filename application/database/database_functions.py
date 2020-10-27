from peewee import *
from .models import Trails
import logging

# Logger
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s %(levelname)s %(message)s', datefmt='%d-%m-%y %H:%M:%S')
log = logging.getLogger('root')


# use these functions to preform actions in the database
# TODO: need to add exception

def add_trail(name, leng, summ, natl_pk, state):
    try:

        Trails.create(trail_name=name, trail_len=leng, trail_sum=summ, natl_park=natl_pk,
                      state=state)
        log.info(f'Added Trail: {name}  to the database.')
    except Exception as e:
        log.exception(f'Error occurred. More detail: {e}')
        raise e


def delete_trail_by_id(trail_id):
    query = Trails.delete().where(Trails.trail_id == trail_id)
    query.execute()


def delete_everything():
    """ Deletes all trails from database"""
    Trails.delete().execute()


def get_all_saved_trails():
    """ Returns everything in db"""
    query_01 = Trails.select()
    all_trails = list()

    for i in query_01:
        all_trails.append(i)
        result = str(i)


    return all_trails


# def get_id_by_trail_name(name):
#
#     trail_id = Trails.get_id().where(Trails.trail_name = name)
#     return trail_id


def saved_trail_count():
    """ :returns the number of saved trails in the db """
    return Trails.select().count()
