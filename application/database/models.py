from peewee import *
from .db_config import database_path
# from db_config import database_path
import datetime

db = SqliteDatabase(database_path)


class Trails(Model):
    # DB ID
    trail_id = AutoField()
    # hiking API returned items
    trail_name = CharField(unique=True)
    trail_len = FloatField()
    trail_sum = CharField()

    natl_park = CharField()
    # will save the datetime of the moment it is saved
    date_saved = DateTimeField(default=datetime.datetime.now)
    state = CharField()

    class Meta:
        database = db

    def __str__(self):
        trail_info = dict()
        trail_info['id'] = self.trail_id
        trail_info['name'] = self.trail_name
        trail_info['length'] = self.trail_len
        trail_info['summary'] = self.trail_sum
        trail_info['national_park'] = self.natl_park
        trail_info['state'] = self.state

        return str(trail_info)


def initialize_db():
    db._connect()
    db.create_tables([Trails], safe=True)
