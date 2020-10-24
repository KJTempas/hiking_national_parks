from peewee import *
from .db_config import database_path
# from db_config import database_path
import datetime

db = SqliteDatabase(database_path)

class Trails(Model):

    ## db id
    trail_id = AutoField()
    ## hiking API returned items
    trail_name = CharField()
    trail_len = FloatField()
    trail_difficulty = CharField()
    trail_sum = CharField()
   # trail_img = CharField()
    ## 
    natl_park = CharField()
    # will save the datetime of the moment it is saved
    date_saved = DateTimeField(default=datetime.datetime.now)
    state = CharField()
    

    class Meta:
        database = db


def initialize_db():
    db._connect()
    db.create_tables([Trails], safe=True)





#
# class List:
#     def __init__(self, list, identifier, expiry):
#         self.list = list
#         self.identifier = identifier
#         self.expiry = expiry