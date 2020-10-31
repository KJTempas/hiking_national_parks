import peewee
from peewee import *
from .models import Trails
import logging

# Logger
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s %(levelname)s %(message)s', datefmt='%d-%m-%y %H:%M:%S')
log = logging.getLogger('root')


# use these functions to preform actions in the database
def add_trail(name, leng, summ, natl_pk, state):
    try:
        Trails.create(trail_name=name, trail_len=leng, trail_sum=summ, natl_park=natl_pk,
                      state=state)
        log.info(f'Added Trail: {name}  to the database.')
    except peewee.IntegrityError as e:
        log.exception(f'Error occurred. More detail: {e}')
        raise e
    except Exception as e:
        log.exception(f'Error occurred. More detail: {e}')
        raise e


def delete_trail_by_id(trail_id):
    try:
        query = Trails.delete().where(Trails.trail_id == trail_id)
        query.execute()
    except Exception as e:
        log.exception(f'Error occurred. More detail: {e}')
        raise e


def delete_everything():
    """ Deletes all trails from database"""
    try:
        Trails.delete().execute()
    except Exception as e:
        log.exception(f'Error occurred. More detail: {e}')
        raise e


def get_all_saved_trails():
    """ Returns everything in db"""
    try:
        query_01 = Trails.select()
        all_trails = list()

        for i in query_01:
            all_trails.append(i)
            result = str(i)
        return all_trails
    except Exception as e:
        log.exception(f'Error occurred. More detail: {e}')
        raise e


def saved_trail_count():
    """ :returns the number of saved trails in the db """
    try:
        counts = Trails.select().count()
        return counts
    except Exception as e:
        log.exception(f'Error occurred. More detail: {e}')
        raise e


