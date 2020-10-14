from peewee import *

db = SqliteDatabase(hiking_trails.db)

class Trails(Model):

    # db id
    trail_id = AutoField()
    # hiking API returned items
    trail_name = CharField()
    trail_len = FloatField()
    trail_difficulty = CharField()
    trail_sum = CharField()
    trail_img = CharField()
    ##
    natl_park = CharField()
    date_saved = DateTimeField()
    state = CharField()
    

    class Meta:
        database = db




db.connect()
db.create_tables([Trails])