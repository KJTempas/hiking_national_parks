from peewee import *
from database_config import database_path
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




db.connect()
db.create_tables([Trails])jhg