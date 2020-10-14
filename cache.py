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
#need 2 add methods ? one for hiking info an one for weather?

#def add_hiking(cachable):  #identifier is the key
def add(object, identifier,   texpiry): 
    memcache_client.set(identifier, object, expire = 1036000) 

def add_weather(cachable):
    memcache_client.set(cachable.identifier, cachable, expire = 36000)#3600sec = 1 hour

def fetch(identifier, cls):
    cached_object = memcache_client.get(identifier)
    return cached_object

def fetch_weather(identifier, cls):
    cached_object = memcache_client.get(identifier)
    return cached_object