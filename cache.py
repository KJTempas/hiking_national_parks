import time
from datetime import datetime
import json
import sys
from pymemcache.client.base import Client
from pymemcache import serde


#pickle converts objects to binary (serializes and deserializes)
# cache is stored in binary
#connect to memcached client
memcache_client = Client('localhost', serde=serde.pickle_serde)
"""
memcache saves in key/value pairs
these add and fetch  method will work for caching natlpark, hiking and weather info
object is the data to be cached; add is a .set() and fetch is .get()
identifier (the key) will be stateCode for natlparks, lat+long? for hiking, and date for weather
expiry will vary by API; 1 month(2,628,000 sec)for natlparks and hiking and 1 day (86400) for weather
need to type 'memcached' in terminal to activate memcache
"""
# in controller this fetch() will be called, and if the result is None, a new API call 
#will be made; when the data is retrieved, add() will be called to set it in the cache
def add(object, identifier, expiry): 
    memcache_client.set(identifier, object, expire =expiry) 


#def fetch(identifier, cls):
def fetch(identifier):
    cached_object = memcache_client.get(identifier) #.get(key)
    return cached_object

